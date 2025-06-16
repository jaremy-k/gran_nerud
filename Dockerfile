FROM python:3.12

RUN mkdir /calculate_price

WORKDIR /calculate_price

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /calculate_price/docker/*.sh

CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:5003"]