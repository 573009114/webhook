FROM docker.io/novopl/python36
MAINTAINER  Hao.Wen sms webhook <573009114@QQ.COM>

WORKDIR /home/

COPY . .

RUN pip3 install -r requirements.txt  && \
    chmod +x /home/app.py

CMD  ["python3","app.py"]
