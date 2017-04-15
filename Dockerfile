FROM tiangolo/uwsgi-nginx-flask:flask

COPY . .

RUN pip install -r requirements.txt
