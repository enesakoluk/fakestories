FROM python:3.10.0
# FROM python:3.8.3-alpine
# FROM python:3.6-slim
# FROM python:3.9-alpine
# FROM python:3.8.3-slim-buster
             
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN pip install --upgrade pip
COPY requirements.txt /code/

RUN pip install -r requirements.txt
COPY . /code/

EXPOSE 8000

CMD ["python" ,"manage.py" ,"migrate", "&&","python", "manage.py", "runserver", "0.0.0.0:8000"]
# docker build . -t test 
# docker run test
#docker container ps
#docker exec -it <container_id> python manage.py createsuperuser
#python manage.py createsuperuser --email admin@example.com --username admin
