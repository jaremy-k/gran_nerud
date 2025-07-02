FROM python:3.12

RUN mkdir /grand_nerud

WORKDIR /grand_nerud

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /grand_nerud/docker/*.sh

CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:5003"]