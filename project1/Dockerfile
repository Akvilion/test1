FROM python:3.8.3-alpine

WORKDIR /test1

COPY . .

RUN apk add build-base
# RUN apk add make

export FLASK_APP start.py

RUN pip3 install -r requirements.txt

EXPOSE 5000

WORKDIR /test1/project1/

CMD ["python3", "start.py", "--host=0.0.0.0:5000"]