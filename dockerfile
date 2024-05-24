
FROM python:3.10

WORKDIR /app

COPY app.py .

RUN pip install -r requirements.txt

CMD ["python", "app.py"]