FROM python:3.8-slim-buster

WORKDIR /python-docker

COPY . .

ENV FLASK_APP=main.py


RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]