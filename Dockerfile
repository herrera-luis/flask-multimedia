FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1

# Install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt 

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"
ENV FLASK_APP "src/src/app.py"


EXPOSE 9000

CMD ["flask", "run"]