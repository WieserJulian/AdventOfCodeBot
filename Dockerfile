FROM python:3.11
LABEL authors="wiju"

WORKDIR /usr/src/app

COPY assets ./assets
COPY src ./src
COPY main.py ./
COPY requirements.txt ./

RUN pip install -r requirements.txt
RUN apt update
RUN apt upgrade
RUN apt-get install sqlite3
CMD ["python", "main.py"]
