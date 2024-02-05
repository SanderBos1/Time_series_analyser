start with the following command:
docker compose -f docker-compose.yml up --detach

push to dockerhub:
docker build -t time_series_analyzer .
docker tag time_series_analyzer:latest sanderbos/time_series_analyzer:0.0.1
docker push sanderbos/time_series_analyzer:0.0.1
