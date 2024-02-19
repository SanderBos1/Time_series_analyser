FROM python:latest

COPY connections connections
COPY ts_app ts_app
COPY data data
COPY ts_images ts_images
COPY python_classes python_classes
COPY requirements.txt requirements.txt
COPY master.py master.py

RUN pip install -r requirements.txt
ENTRYPOINT [ "python3" ]
EXPOSE 8000
CMD ["master.py" ]