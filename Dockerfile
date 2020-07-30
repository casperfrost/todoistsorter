FROM python:3.8-alpine

ADD . /

RUN pip install -r requirements.txt

EXPOSE 5000

CMD [ "python", "./WebService.py" ]