FROM python:3.6.1-alpine

WORKDIR /app

RUN apk --update add git curl rsync

RUN git config --global user.email "you@example.com"
RUN git config --global user.name "Your Name"

RUN pip3 install pipenv
ADD Pipfile Pipfile.lock ./
RUN pipenv install

RUN curl https://get.helm.sh/helm-v3.1.0-linux-amd64.tar.gz --output helm_bin.tar.gz
RUN tar -zxvf helm_bin.tar.gz
RUN mv linux-amd64/helm /usr/local/bin
RUN rm helm_bin.tar.gz
RUN rm -rf linux-amd64

ADD . .

CMD ["pipenv", "run", "python3", "-m", "unittest"]