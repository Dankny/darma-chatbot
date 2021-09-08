FROM rasa/rasa-sdk:2.6.0

USER root 

RUN pip3 install recognizers-text-suite 
COPY actions/requirements.txt ./
RUN pip3 install -r requirements.txt

USER 1001