FROM python:3.11-slim

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./src ./src
EXPOSE 8080

CMD ["flask","--app", "./src/client" ,"--debug","run","--host=0.0.0.0", "--port=8080" ]
