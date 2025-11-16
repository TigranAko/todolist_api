FROM python:3.14.0-alpine3.22
# RUN groupadd -r groupfastapi && useradd -r -g groupfastapi userfa
RUN apk add --no-cache gcc musl-dev libpq-dev 

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

RUN pip install --upgrade pip
WORKDIR /app/www/todolist
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# USER userfa
