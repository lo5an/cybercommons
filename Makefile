dc_config/secrets.env:
# Creating secrets file for editing
ifndef EDITOR
ifeq ($(strip $(shell which nano)),)
$(error dc_config/secrets.env will need to be manually created. Copy dc_config/secrets_template.env as a starting point)
endif
endif
	@cp dc_config/secrets_template.env dc_config/secrets.env
	@$${EDITOR:-nano} dc_config/secrets.env


include dc_config/cybercom_config.env
include dc_config/secrets.env

# Set GITPOD_PORT to 8080 if run in gitpod
ifneq ($(strip $(GITPOD_WORKSPACE_ID)),)
	GITPOD_PORT = 8080
	ALLOWED_HOSTS = .gitpod.io,localhost
endif

ifeq ($(strip $(shell docker compose > /dev/null 2>&1 && echo 0)),0)
	COMPOSE = docker compose
else
	COMPOSE = docker-compose
endif

ifeq ($(USE_LOCAL_MONGO),True)
$(info using local mongo database)
	COMPOSE := $(COMPOSE) --profile mongo --compatibility
	API-CONTAINER = cybercom_api
	CELERY-CONTAINER = cybercom_celery
else
$(info using external mongo database)
	COMPOSE := $(COMPOSE) --profile external_mongo --compatibility
	API-CONTAINER = cybercom_api_external_mongodb
	CELERY-CONTAINER = cybercom_celery_external_mongodb
endif

COMPOSE_INIT = $(COMPOSE) -f dc_config/images/docker-compose-init.yml
CERTBOT_INIT = $(COMPOSE) -f dc_config/images/certbot-initialization.yml
DJANGO_MANAGE = $(COMPOSE) run --rm cybercom_api ./manage.py

SHELL = /bin/bash

.PHONY: init intidb initssl cert_dates superuser migrate flush init_certbot renew_certbot \
	shell apishell celeryshell dbshell build force_build run stop test restart_api collectstatic

.EXPORT_ALL_VARIABLES:
UID=$(shell id $(LOCAL_USER) -u)
GID=$(shell id $(LOCAL_USER) -g)

init: 
	$(COMPOSE_INIT) build
	$(COMPOSE_INIT) up
	$(COMPOSE_INIT) down

initdb:
	$(COMPOSE_INIT) up cybercom_mongo_init
	$(COMPOSE_INIT) down

initssl:
	$(COMPOSE_INIT) build cybercom_openssl_init
	$(COMPOSE_INIT) up cybercom_openssl_init
	$(COMPOSE_INIT) down

cert_dates:
	# Show valid date ranges for backend ssl certificates
	@$(COMPOSE_INIT) run --rm cybercom_openssl_init openssl x509 -noout -dates -in /ssl/server/cert.pem

collectstatic: 
	@mkdir -p web/static
	@$(DJANGO_MANAGE) collectstatic --noinput

superuser:
	@$(DJANGO_MANAGE) createsuperuser 

migrate:
	@$(DJANGO_MANAGE) migrate

flush:
	@$(DJANGO_MANAGE) flush

init_certbot:
	$(CERTBOT_INIT) build
	$(CERTBOT_INIT) up --abort-on-container-exit
	$(CERTBOT_INIT) down

renew_certbot:
	$(CERTBOT_INIT) run --rm cybercom_certbot
	# This requires an init process running in the container
	# https://docs.docker.com/compose/compose-file/compose-file-v3/#init
	@$(COMPOSE) exec cybercom_nginx nginx -s reload

shell:
	@echo "Loading new shell with configured environment"
	@$(SHELL)

apishell:
	@echo "Launching shell into Django"
	@$(COMPOSE) exec $(API-CONTAINER) python manage.py shell

celeryshell:
	@echo "Lanuching shell into Celery"
	@$(COMPOSE) exec $(CELERY-CONTAINER) celery shell

dbshell:
	@echo "Launching shell into MongoDB"
	@$(COMPOSE) run --rm cybercom_mongo mongosh  \
		--tls \
		--host $$MONGO_HOST \
		--tlsCertificateKeyFile $$MONGO_CERT_KEY_FILE \
		--tlsCAFile $$MONGO_CA_FILE \
		--username $$MONGO_USERNAME \
		--password $$MONGO_PASSWORD

build:
	@$(COMPOSE) build

force_build:
	@$(COMPOSE) build --no-cache

run:
	@$(COMPOSE) up -d

stop:
	@$(COMPOSE) down	
test:
	@$(COMPOSE) exec $(API-CONTAINER) python -Wa manage.py test

restart_api:
	@$(COMPOSE) restart $(API-CONTAINER)

collectstatic: 
	@mkdir -p web/static
	@$(COMPOSE) run --rm $(API-CONTAINER) ./manage.py collectstatic --noinput
