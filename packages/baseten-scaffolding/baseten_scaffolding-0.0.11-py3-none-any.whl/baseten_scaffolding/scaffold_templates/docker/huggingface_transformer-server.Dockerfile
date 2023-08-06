FROM baseten/baseten-huggingface-transformer-server-base:latest

COPY ./src/server_requirements.txt server_requirements.txt
RUN pip install -r server_requirements.txt

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

ENV PORT 8080
ENV APP_HOME /app

WORKDIR $APP_HOME
COPY ./src .

# BaseTen specific build arguments and environment variables
ARG RUNTIME_ENV
ARG SENTRY_URL
ENV RUNTIME_ENV=$RUNTIME_ENV
ENV SENTRY_URL=$SENTRY_URL

ARG hf_task
ARG has_hybrid_args
ARG has_named_args
ENV hf_task=$hf_task
ENV has_hybrid_args=$has_hybrid_args
ENV has_named_args=$has_named_args

CMD exec python3 inference_server.py
