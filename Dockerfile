FROM python:3.10



COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY app.py ./app.py

CMD ["python", "app.py"]