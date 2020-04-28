FROM ubuntu:18.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    rm -rf /var/lib/apt/lists/*

RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update && apt-get install -y --force-yes \
      ruby-full python3.6 python3-pip rsync curl git \
      zlib1g-dev libssl-dev libreadline-dev libyaml-dev libxml2-dev libxslt-dev \
      && apt-get clean

RUN git clone https://github.com/sstephenson/rbenv.git /root/.rbenv
RUN git clone https://github.com/sstephenson/ruby-build.git /root/.rbenv/plugins/ruby-build
RUN /root/.rbenv/plugins/ruby-build/install.sh
ENV PATH /root/.rbenv/bin:$PATH
RUN echo 'eval "$(rbenv init -)"' >> /etc/profile.d/rbenv.sh # or /etc/profile
RUN echo 'eval "$(rbenv init -)"' >> .bashrc

ENV CONFIGURE_OPTS --disable-install-doc
ADD ./versions.txt /root/versions.txt
RUN xargs -L 1 rbenv install < /root/versions.txt

RUN echo 'gem: --no-rdoc --no-ri' >> /.gemrc
RUN bash -l -c 'for v in $(cat /root/versions.txt); do rbenv global $v; gem install bundler; done'

ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    TEST_TMP_ROOT=/app/lols

RUN pip3 install pipenv
ADD Pipfile Pipfile.lock ./
RUN pipenv install

RUN curl https://get.helm.sh/helm-v3.1.0-linux-amd64.tar.gz --output helm_bin.tar.gz
RUN tar -zxvf helm_bin.tar.gz
RUN mv linux-amd64/helm /usr/local/bin
RUN rm helm_bin.tar.gz
RUN rm -rf linux-amd64

RUN git config --global user.email "you@example.com"; \
    git config --global user.name "Your Name"

ADD . .

RUN mkdir /app/lols

ENTRYPOINT ["./docker-cmd.sh"]