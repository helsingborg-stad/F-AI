# 📦 buildtime-image:
FROM python:3.11 AS buildtime-image

# RUN apt-get update
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc

# cache packages for 🕹️ with 👾 virtualenv:
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app
COPY /src/planning_permission/requirements.txt .
RUN pip install -q -r requirements.txt

# 🕹️ runtime-image: can be re-built with cached 📦
FROM python:3.11 AS runtime-image

COPY --from=buildtime-image /opt/venv /opt/venv
COPY --from=buildtime-image /app /app

# we shall not forget our 👾 virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

ARG CHAINLIT_PORT=80
ENV CHAINLIT_PORT=$CHAINLIT_PORT

WORKDIR /app
COPY /src .
COPY /src/planning_permission/.chainlit .
COPY /src/planning_permission/chainlit.md .
EXPOSE ${CHAINLIT_PORT}
ENTRYPOINT python -m chainlit run planning_permission/app_main_stream.py -h --port ${CHAINLIT_PORT}