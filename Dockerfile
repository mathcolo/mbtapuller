FROM tiangolo/uwsgi-nginx-flask:flask

COPY . /app
RUN pip install requests sqlalchemy vcrpy geopy
RUN mv /app/app.py /app/main.py

RUN python /app/initial_setup.py
