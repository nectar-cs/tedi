FROM python:3.6

RUN apt-get update && apt-get install git \
                                      curl

ADD requirements.txt .
RUN pip3 install -r requirements.txt

RUN curl https://get.helm.sh/helm-v3.1.0-linux-amd64.tar.gz --output helm_bin.tar.gz
RUN tar -zxvf helm_bin.tar.gz
RUN mv linux-amd64/helm /usr/local/bin
RUN rm helm_bin.tar.gz
RUN rm -rf linux-amd64

RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl
RUN chmod +x ./kubectl
RUN mv ./kubectl /usr/local/bin/kubectl
RUN kubectl version --client

ADD helm-ted/main.py /nectar/
#ENTRYPOINT ["python", "nectar/main.py"]