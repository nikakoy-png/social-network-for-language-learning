FROM python:3.12

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN python manage.py makemigrations
RUN python manage.py migrate

CMD ["uvicorn", "Registry.asgi:application", "--port", "8001"]
