FROM ubuntu

COPY . /pet

WORKDIR /pet/pet

RUN apt-get update
RUN apt-get install -y python3-pip
RUN pip install -r requirements.txt

#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
CMD [ "python3", "app.py"]
