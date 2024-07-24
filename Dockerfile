FROM python:3.10.14

WORKDIR /usr/src/app
EXPOSE 5000

RUN apt-get update
COPY requirements.txt ./
RUN python3 -m venv venv
RUN . venv/bin/activate
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./app.py" ]