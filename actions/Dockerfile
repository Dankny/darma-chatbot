FROM rasa/rasa-sdk:2.6.0


WORKDIR /app
COPY ./app actions/requirements.txt 

USER root 

RUN pip3 install recognizers-text-suite 
RUN pip3 install -r requirements.txt

USER 1001