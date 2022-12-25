# Dockerfile
FROM python:3.9-buster
COPY Pipfile Pipfile.lock ./
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy

WORKDIR /home/app

COPY backend/ backend/
COPY app/ app/
COPY db.sqlite3 . 
COPY manage.py .


ENTRYPOINT ["python3"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]

