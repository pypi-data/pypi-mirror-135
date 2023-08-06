# Baseten Scaffold

A baseten scaffold is a context for building a container for serving predictions from a model. The scaffolds are
designed to work seamlessly with in-memory models from supported model frameworks while maintaining the ability to
serve predictions for more complex scenarios. The scaffolds can be created local to the environment of the client
for introspection and any required debugging and then when ready, uploaded in our serving environment or onto another
container serving platform

## Requirements
* Python 3
* docker

Compatable but not necessary
* sklearn
* keras
* pytorch

The package assumes a familiarity with docker concepts and web servers.

# Tutorials
## Creating a Simple Scaffold

As a simple example; here we will look at the creation of a scaffold using an sklearn classifier. We start with a
trained model described below.

```python
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

iris = load_iris()
data_x = iris['data']
data_y = iris['target']
rfc_model = RandomForestClassifier()
rfc_model.fit(data_x, data_y)
```

And now we can create a scaffold from the in-memory model
```python
from baseten_scaffolding.scaffold.build import scaffold
scaffold = scaffold(rfc_model, target_directory='test_rfc')
```

This will produce a folder `test_rfc/` relative to the current directory which will contain all the elements required
to build a scaffold container. In fact, it can produce the command to build the container.

```python
>> scaffold.docker_build_string
'docker build  -f test_rfc/sklearn-server.Dockerfile test_rfc'
```

It is wise to append a target via `-t <name>` to the build. You can build and run the container like so

```commandline
docker build  -f test_rfc/sklearn-server.Dockerfile test_rfc -t test_rfc
docker run --rm  -p 8080:8080 -t test_rfc
```

And then curl a POST to the server on your localhost

```commandline
curl -H 'Content-Type: application/json' -d '{"instances": [[0,0,0,0]]}' -X POST http://localhost:8080/v1/models/model:predict
```

Congrats! You just built a scaffold and tested it locally.

 ## Extending a Scaffold

 As a motivating example we will look at the case of a hybrid model where we use keras for modeling with sklearn for
 preprocessing. In this example we will train a model to determine the MPG of an automobile using the
  [Auto MPG dataset](http://archive.ics.uci.edu/ml/datasets/Auto+MPG).

 The model will be a simple feed forward network in keras with a standard scaler from sklearn.

```python
import pandas as pd
import tensorflow as tf
from sklearn import preprocessing

from tensorflow.keras import layers

url = 'http://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data'

feature_names =[
    'MPG', 'Cylinders', 'Displacement', 'Horsepower', 'Weight', 'Acceleration', 'Model Year',
]

column_names = feature_names + ['Origin']


raw_dataset = pd.read_csv(url, names=column_names,
                          na_values='?', comment='\t',
                          sep=' ', skipinitialspace=True)

dataset = raw_dataset.copy()
dataset = dataset.dropna()

train_dataset = dataset.sample(frac=0.8, random_state=0)
test_dataset = dataset.drop(train_dataset.index)


train_features = train_dataset.copy().loc[:, feature_names]
test_features = test_dataset.copy().loc[:, feature_names]

train_labels = train_features.pop('MPG')
test_labels = test_features.pop('MPG')

scaler = preprocessing.StandardScaler().fit(train_features)

tf_model = tf.keras.Sequential([
    layers.Dense(units=8),
    layers.Dense(units=1)
])
tf_model.compile(
    optimizer=tf.optimizers.Adam(learning_rate=0.1),
    loss='mean_absolute_error'
)

history = tf_model.fit(
    scaler.transform(train_features),
    train_labels,
    epochs=100,
    # suppress logging
    verbose=0,
    # Calculate validation results on 20% of the training data
    validation_split = 0.2
)
 ```

With our trained model; we can create a scaffold for it.

```python
from baseten_scaffolding.scaffold.build import scaffold
scaffold = scaffold(tf_model, target_directory='test_keras')
```

But if we were to serve the model like this, the responses would be garbage-out because we haven't scaled the inputs to feed into the model. To do so we are going to make some edits in the scaffold.

First, we will save a binary of the scaler object we created in the model training phase

```python
import joblib
joblib.dump(scaler, 'scaler.joblib')
```

Afterwards we will place the `scaler.joblib` file into the `data/` directory in the scaffold.

```commandline
mv scaler.joblib test_keras/data/
```

By default the inference of a keras model will produce a requirements file that only has `tensorflow` as a requirement. So we will add the following lines to our `model_framework_requirements.txt`. Ours were inferred from a `pip freeze` and might be different than your system.

```commandline
joblib==1.0.1
scikit-learn==0.24.2
```

Then we will make some edits to the scaffold's code to enable it to use the scaler. There are two files that live inside the scaffold `model.py` and `serve.py`. We will make the following changes to the functions `predict` and `load` inside of `model.py`
```python
import os
import joblib
...
def load(self):
    self._scaler = joblib.load(os.path.join('data', 'scaler.joblib'))
    ...

def predict(self):
    ...
    inputs = self._scaler.transform(np.array(instances))
    ...
```

Now to test the scaffold locally we can build the docker container, run it, and POST a prediction to it.

We build with a target (`scaffold.docker_build_string` will produce something like this)
```commandline
docker build  -f test_keras/keras-server.Dockerfile test_keras -t test_keras
```

We run with the server's port's forwarded
```commandline
docker run --rm  -p 8080:8080 -t test_keras
```
After verifying that the server runs fine, we can test with a CURL
```commandline
curl -H 'Content-Type: application/json' -d '{"instances": [[0,0,0,0,0,0]]}' -X POST http://localhost:8080/v1/models/model:predict
```

## Usage outside of the docker image
It is possible to use the scaffold object to test locally before outside of the docker image. This requires `kfserving < 0.7.0` to be present in the current python environment.
Using the [simple scaffold created in the first example](#creating-a-simple-scaffold) as a basis, we can do the following:

```python
from baseten_scaffolding.scaffold.build import scaffold
scaffold = scaffold(rfc_model, target_directory='test_rfc')

prediction = scaffold.predict([[0,0,0,0]])
```

Calling the `predict` method will execute the whole prediction flow, which includes `preprocess` and `postprocess` methods.

# Discussion
## Scaffold Architecture

At a high level this tool builds on top of existing frameworks. Out of the box we support `sklearn`, `keras`, and
`pytorch` models. Our serving infrastructure is based on `kfserving` with some opinions. However the architecture of the scaffold is
suggestive and not prescriptive. The idea of the package is that one can make changes to the structure locally and test
it. Significant divergence from the suggestions might lead to incompatibility with Baseten's serving environment, but
might be required for other usecases.

## Scaffold Structure

Below is the structure of a `sklearn` scaffold created via the factory method `scaffold` with descriptions alongside.
The structure between this model frameworks and others are largely consistent.
The `src` directory becomes the `/app` directory inside the container, which is the working directory of the container.

```
scaffold_directory
  src/common/ - a Python package that contains BaseTen utilities on top of kfserving
  src/server/ - a Python package that contains classes for the model server
  src/server/inference_model.py - a template of a KFModel class for inference
  src/model/ - a Python package that contains the serialized model and is a destination for code
  src/data/ - this folder is a destination for non-cod data required by the model
  src/inference_server.py - the main entry point for the application.
  requirements.txt - a PIP requirements file
  sklearn-server.Dockerfile - the Dockerfile that defines the build for the container
  REAME.md - a helpful explanation file for the scaffold
  config.yaml - information used in the BaseTen build and deploy process
 ```

 In general we'd encourage people to package any subsequent code into `model` folder and other binaries into the `data` directory. The
 `requirements.txt` file is a PIP requirements file that can be edited to add more packages. The
  `sklearn-server.Dockerfile` contains the instructions from which the container is built.

 Everything in here is a suggestion. The end user has full control of all the artifacts within that directory by
 design. However, if you take too many liberties we can't guarantee that deployment into the baseten serving
 environment will be seamless, but the package is intended for usage apart from baseten.

## Environment Replication

The default `scaffold` factory methods do inference on the Python runtime environment for required libraries. This means that
it introspects the Python runtime and infers the versions of required libraries for respective framework and environments then populates
the `requirements.txt` with the inferred definitions. Any subsequent extension beyond what is inferred should be
added to `requirements.txt`

## Model Serialization

Each model framework has a definition that extends from the class `WrittenModelScaffoldDefinition` by which framework
specific serialization is defined by the function `serialize_model_to_directory`.

## Baseten Model

The code for this will be in `server/interfence_model.py`. The logic flow is such that there are the following methods that are run
 in order

* `load` - This is run once when the process is started and is a good place to do any expensive computations or data loading that needs to be run once

With these methods running on every request in order.
* `preprocess` - This is an ideal place to place any input level feature transformed that might not be encapsulated by the model object.
* `predict` - This is the main prediction method; by default we support most JSON serializable objects in addition to numpy objects.
* `postprecess` - This is an ideal place to place any output level feature transforms that might not be encapsulated by the model.


## Request & Response Serialization

The default path `v1/models/model:predict` will consume and produce JSON with some liberties taken for complex types

The path `v1/models/model:predict_binary` will consume and produce a Baseten opinionated binary serialization. It is
largely based on `msgpack` and can be seen at `scaffold_templates/common/serialization.py`. This will work natively inside
a baseten workflow.
