FROM python:3.7-slim

RUN apt update && apt full-upgrade -y && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip3 install --upgrade pip && pip3 install -r requirements.txt --no-cache-dir
RUN python manage.py collectstatic --no-input

CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ]
