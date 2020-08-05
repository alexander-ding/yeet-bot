FROM continuumio/anaconda3

RUN conda install -c conda-forge dlib=19.17

COPY requirements.txt /opt/
WORKDIR /opt/

# then get the packages down
RUN pip install -r requirements.txt

COPY . /opt/server/
WORKDIR /opt/server

CMD [ "python", "./bot.py" ]