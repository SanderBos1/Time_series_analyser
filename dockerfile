FROM ubuntu:latest
RUN apt update && \ 
    apt install -y python3-pip 
COPY ts_app ts_app
COPY ts_config ts_config
COPY ts_python ts_python
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
WORKDIR /ts_app
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
