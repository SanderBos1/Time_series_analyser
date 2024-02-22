lint:
	pylint ./ts_app
	pylint ./ts_app/image_creation

activate_vm:
	.\venv\Scripts\activate

requirements:
	pip freeze > requirements.txt


