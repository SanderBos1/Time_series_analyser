lint:
	pylint ./ts_app/

activate_vm:
	.\venv\Scripts\activate

requirements:
	pip freeze > requirements.txt
