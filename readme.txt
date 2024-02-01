start with the following command:
docker compose -f docker-compose.yml up --detach

push to dockerhub:
docker tag time_series_analyser sanderbos/time_series_analyzer:0.0.1
docker push sanderbos/time_series_analyzer:0.0.1
