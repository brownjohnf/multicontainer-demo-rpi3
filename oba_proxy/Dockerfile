FROM arm32v6/python:3-alpine

RUN mkdir /src
WORKDIR /src

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . ./

ENV FLASK_APP index.py
CMD ["python", "-m", "flask", "run"]

