FROM python:3.10



COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY app.py ./app.py
EXPOSE 5000
CMD ["python", "app.py"]

