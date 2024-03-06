FROM python:latest

COPY templates templates
COPY static static
COPY ts_app ts_app
COPY data data
COPY requirements.txt requirements.txt
COPY app.py app.py
RUN pip install -r requirements.txt
ENTRYPOINT [ "python3" ]
EXPOSE 8000
CMD ["app.py"]