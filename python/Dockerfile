FROM python:3.8

ENV http_proxy 'http://tlzshuang:8953890535@oym.proxy.nic.fujitsu.com:8080'
ENV https_proxy 'http://tlzshuang:8953890535@oym.proxy.nic.fujitsu.com:8080'

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#EXPOSE 5000

ENV FLASK_APP ./manage.py

#CMD ["python", "manage.py","run"]
