FROM gcr.io/nectar-bazaar/tedi-base:latest

ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    TEST_TMP_ROOT=/app/lols

RUN pip3 install pipenv
ADD Pipfile Pipfile.lock ./
RUN pipenv install

RUN git config --global user.email "you@example.com"; \
    git config --global user.name "Your Name"

ADD . .

RUN mkdir /app/lols

ENTRYPOINT ["./docker-cmd.sh"]
