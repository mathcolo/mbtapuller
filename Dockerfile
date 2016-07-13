FROM tiangolo/uwsgi-nginx-flask:flask

COPY . /app
RUN pip install requests sqlalchemy vcrpy geopy mysql-python
RUN mv /app/app.py /app/main.py
