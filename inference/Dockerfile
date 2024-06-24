FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
EXPOSE 80
ENV GOOGLE_APPLICATION_CREDENTIALS=alien-hologram-385114-33979343e906.json