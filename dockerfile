FROM ubuntu:latest
RUN apt update && \ 
    apt install -y python3-pip 
COPY . .
RUN pip install -r requirements.txt
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
