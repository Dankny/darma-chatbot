FROM rasa/rasa:2.6.3-full

WORKDIR /app
COPY . /app
COPY ./data /app/data

USER root

RUN chgrp -R root models && chmod -R 770 models
RUN rasa train
USER 1001

VOLUME /app
VOLUME /app/data
VOLUME /app/models

CMD [ "run", "-m","/app/models","--enable-api","--cors","*","--debug" ]