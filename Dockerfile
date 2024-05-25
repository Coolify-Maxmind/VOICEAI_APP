FROM python:3.10



COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY app.py ./app.py
EXPOSE 5000
CMD ["gunicorn","-w","4","--bind","0.0.0.0:5000", "app.py"]

