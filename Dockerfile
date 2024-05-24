FROM python:3.10

WORKDIR /VOICEAI_APP
COPY Dockerfile .
COPY requirements.txt .
COPY app.py .
RUN pip install -r requirements.txt

CMD ["python", "app.py"]