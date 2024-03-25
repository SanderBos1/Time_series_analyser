lint:
	pylint ./ts_app

format:
	black ./ts_app

requirements:
	pip freeze > requirements.txt

install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt