FROM python:3.8-buster
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
CMD ["sh", "/code/migrate_run.sh"]
