FROM python:3.9

WORKDIR /app

COPY ./server/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY ./server /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]
