FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

CMD ["uvicorn", "app.main:app", "--reload"]
