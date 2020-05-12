FROM python:3.7-buster

COPY . ./

RUN apt update
RUN apt install -y ffmpeg
RUN pip install Flask gunicorn google-cloud-secret-manager

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 ohtaigi-slides:app