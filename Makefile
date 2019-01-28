DOCKER_COMPOSE = sudo docker-compose
TOOLS = @$(DOCKER_COMPOSE) run --rm web

build:
	@$(DOCKER_COMPOSE) build

up:
	@$(DOCKER_COMPOSE) up -d --no-recreate

start:
	@$(DOCKER_COMPOSE) up --build

down:
	@$(DOCKER_COMPOSE) down

migrate:
	@$(TOOLS) python3 manage.py migrate

makem:
	@$(TOOLS) python3 manage.py makemigrations

createsu:
	@$(TOOLS) python3 manage.py createsuperuser
	# log:admin pass:admin123

show:
	@$(TOOLS) python3 manage.py showmigrations

db-sh:
	@$(TOOLS) sh

freeze:
	@$(TOOLS) pip3 freeze

test-all:
	@$(DOCKER_COMPOSE) build web
	@$(TOOLS) py.test -sx