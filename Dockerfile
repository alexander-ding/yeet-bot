FROM yuiti/python-dlib

RUN pip install --upgrade pip

COPY requirements.txt /opt/
WORKDIR /opt/

# then get the packages down
RUN pip install -r requirements.txt

COPY . /opt/server/
WORKDIR /opt/server

CMD [ "python", "./bot.py" ]
