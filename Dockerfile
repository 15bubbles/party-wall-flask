FROM python:3.8-buster

COPY . /app
WORKDIR /app

RUN pip install poetry
RUN poetry export --format requirements.txt --output requirements.txt \
  && pip install -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "-c gunicorn.conf.py", "party_wall.app:app"]
