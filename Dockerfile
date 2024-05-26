FROM python:3.10


COPY audios ./audios
COPY requirements.txt ./requirements.txt
COPY vocab.json ./vocab.json
COPY templates ./templates
RUN pip install -r requirements.txt

COPY app.py ./app.py

EXPOSE 3000
CMD ["gunicorn","-w","4","--bind","0.0.0.0:3000", "app:app"]

