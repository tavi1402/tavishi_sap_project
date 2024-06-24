FROM ubuntu:22.04
RUN mkdir /app
COPY . /app
WORKDIR /app
RUN apt update -y
RUN pip install -r requirements.txt
ENV GOOGLE_APPLICATION_CREDENTIALS=alien-hologram-385114-33979343e906.json
ENV AIRFLOW_HOME=/app/airflow
ENV AIRFLOW__CORE__DAGBAG_IMPORT_TIMEOUT=1000
ENV AIRFLOW__CORE__ENABLE_XCOM_PICKLING=True
ENV AIRFLOW__CORE__EXECUTOR=LocalExecutor
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False
ENV no_proxy=*
ENV GCS_PATH=tavishi_sap_project

ENV TOKENIZERS_PARALLELISM=False
RUN python3 -m airflow db init
RUN python3 -m airflow users create -e tavish@gmail.com -f tavish -l tavish -p tavish@iqfm -r Admin -u tavish
RUN chmod 777 start_airflow.sh
RUN apt install azure-cli -y
ENTRYPOINT [ "/bin/sh" ]
CMD [ "./start_airflow.sh" ]
