# Dockerfile

FROM python:3.9-buster
COPY Pipfile Pipfile.lock ./
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy

WORKDIR /home/app

COPY backend .


CMD [ "python",  "manage.py", "runserver" ]


