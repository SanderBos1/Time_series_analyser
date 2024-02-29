Welcome to the Flask time-series analyzer.
This is my first Flask project with the aim of learning html, css, flask and making connecctions using these technqiues.
This web applications aims to help with the analyses of time-series data.
Users can upload csv files in certain formats and can use multiple functions to analyze this data.
Since it is a learning project, it will gradually become larger and more useful!
Feel free to report any bugs and or issue with the program, it will help me learn.

To execute this program you have to do the following steps.
 - Download the docker-compose file using this link:
	https://github.com/SanderBos1/Time_series_analyser/blob/main/docker-compose.yml
- Save this compose file into a new directory
- In the new directory create a .env file and and define the following parameters.
	SECRET_KEY
	POSTGRES_USER
	POSTGRES_PASSWORD
	POSTGRES_DB
	POSTGRES_PORT
- Execute the folowing command in the created directory:
	docker compose -f docker-compose.yml up --detach
- run the following commands in your flask container
	flask db init
	flask db migrate
	flask db upgrade
