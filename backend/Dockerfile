FROM python:3.11-slim
WORKDIR /app

RUN pip install pip==23.1.2

COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

COPY . .

COPY ./entrypoint.sh /
ENTRYPOINT [ "sh", "/entrypoint.sh" ]  