FROM python:3.11-slim

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./src ./src
EXPOSE 8000

CMD [ "uvicorn", "src.server:app", "--host", "localhost", "--port", "8000", "--reload" ]