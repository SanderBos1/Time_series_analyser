set directory=%CD%


cd %directory%

REM remove old containers, volumes and images

docker container stop time_series_analyser
docker container rm time_series_analyser 
docker container stop time_series_analyser-postgres-1
docker container rm  time_series_analyser-postgres-1

docker volume remove time_series_analyser_saved-datesets
docker volume remove time_series_analyser_postgres-db
docker rmi sanderbos/time_series_analyser:0.0.1 

REM push to dockerhub:


docker build -t time_series_analyser .
docker tag time_series_analyser:latest sanderbos/time_series_analyser:0.0.1
docker push sanderbos/time_series_analyser:0.0.1
docker compose -f docker-compose.yml up --detach
