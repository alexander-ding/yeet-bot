FROM python:3.6

# calm down and do some basics
RUN apt-get update && apt-get install gcc -y && apt-get -y install cmake

COPY requirements.txt /opt/
WORKDIR /opt/

# then get the packages down
RUN pip install -r requirements.txt

COPY . /opt/server/
WORKDIR /opt/server

CMD [ "python", "./bot.py" ]