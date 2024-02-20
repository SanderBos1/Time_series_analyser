FROM python:latest

COPY ts_app ts_app
COPY data data
COPY requirements.txt requirements.txt
COPY app.py app.py
COPY migrations migrations
RUN pip install -r requirements.txt
ENTRYPOINT [ "python3" ]
RUN flask db upgrade

EXPOSE 8000
CMD ["app.py" ]