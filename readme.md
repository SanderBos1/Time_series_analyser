# Welcome to the Flask time-series analyser.

Welcome to the Flask Time-Series Analyser, a project created with the aim of learning HTML, CSS, Flask, and data analysis techniques.
This web application is designed to assist with the analysis of time-series data, 
providing users with the ability to upload CSV files in specific formats and utilize various functions to analyze the data.
As this project is a learning endeavor, it will continue to evolve and become more robust over time, offering increasingly useful features.
Your feedback is greatly appreciated; feel free to report any bugs or issues you encounter, as they will contribute to my learning process.

# Getting Started

To execute this program you have to do the following steps.

1. ### Download the docker-compose:

Download the Docker Compose file from  [link](https://github.com/SanderBos1/Time_series_analyser/blob/main/docker-compose.yml)
	
2. ###  Set Up Your Environment:
Save the downloaded compose file into a new directory. 
Then, create a .env file within the same directory and define the following parameters:
* SECRET_KEY
* POSTGRES_USER
* POSTGRES_PASSWORD
* POSTGRES_DB
* POSTGRES_PORT

3. ### Start the Docker Containers:
Execute the following command in the created directory to start the Docker containers:

	docker compose -f docker-compose.yml up --detach
4. ### Initialize the Database:
Once the Docker containers are up and running, run the following commands in your Flask container to initialize the database:	
* flask db init
* flask db migrate
* flask db upgrade
