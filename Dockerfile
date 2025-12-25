FROM python:3.14.2-alpine

COPY ./sqltest/ /root/sqltest/
RUN pip install pytest 

CMD ["ash"]