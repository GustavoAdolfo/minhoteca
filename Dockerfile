FROM python:3.9-alpine
ENV PYTHONUNBUFFERED=1

WORKDIR /minhoteca
COPY ./requirements.txt
RUN pip install -r requirements.txt
COPY . .
RUN python3 manage.py migrate
RUN python3 manage.py collectstatic --noinput
CMD python3 manage.py runserver 0.0.0.0:80
