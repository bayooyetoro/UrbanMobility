FROM apache/spark:4.2.1 AS spark
FROM apache/airflow:3.3.2-python3.12

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends openjdk-17-jre-headless \
    && JAVA_BIN="$(readlink -f "$(command -v java)")" \
    && ln -s "${JAVA_BIN%/bin/java}" /usr/lib/jvm/default-java \
    && rm -rf /var/lib/apt/lists/*

COPY --from=spark /opt/spark /opt/spark

ENV SPARK_HOME=/opt/spark
ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH="${SPARK_HOME}/bin:${PATH}"

USER airflow

ARG AIRFLOW_VERSION=3.3.2
ARG PYTHON_VERSION=3.12

RUN pip install --no-cache-dir \
    "apache-airflow==${AIRFLOW_VERSION}" \
    apache-airflow-providers-apache-spark \
    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"