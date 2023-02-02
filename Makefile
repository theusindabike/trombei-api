run:
	docker-compose down --volumes && docker-compose up --build

run_staging:
	docker-compose -f docker-compose.staging.yaml down --volumes && docker-compose -f docker-compose.staging.yaml up --build

run_aws:
	docker-compose -f docker-compose.aws.yaml down && docker-compose -f docker-compose.aws.yaml up --build

tests:
	docker-compose down --volumes && docker-compose build && docker-compose run --rm web sh -c "python manage.py test --nomigrations --noinput"

lint:
	docker-compose build && docker-compose run --rm web  sh -c "flake8"

docker_exec:
	docker exec -it trombei_api /bin/sh

aws_logs:
	docker logs nginx_proxy -n 100 -f

create_superuser_local:
	docker run trombei_api sh -c "python manage.py createsuperuser --no-input"

clean_docker:
	docker rm -f $(docker ps -a -q)

migrations:
	python manage.py makemigrations && python manage.py migrate

clean_migrations:
	find . -path "*/trombei_api/*/migrations/*.py" -not -name "__init__.py" -delete && find . -path "*/trombei_api/*/migrations/*.pyc"  -delete