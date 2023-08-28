# Makefile

# Docker Compose commands
DC=docker-compose
DC_BUILD=$(DC) build
DC_UP=$(DC) up
DC_DOWN=$(DC) down
DC_RUN=$(DC) run --rm app sh -c
FLAKE8=$(DC_RUN) "flake8"
STARTPROJECT=$(DC_RUN) django-admin startproject
TEST="python manage.py test"


default: help

dcup:
	$(DC_UP)
up: dcup

dcdown:
	$(DC_DOWN)
down: dcdown

dcbuild:
	$(DC_BUILD)
build: dcbuild

test:
	$(DC_RUN) "python manage.py test && flake8"
t: test


createproject:
ifeq ($(filter-out $@,$(MAKECMDGOALS)),)
	@echo "Usage: make createproject project_name [optional: .]"
else
	$(DC_RUN) "django-admin startproject $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))"
endif
cp: createproject

createapp:
ifeq ($(filter-out $@,$(MAKECMDGOALS)),)
	@echo "Usage: make createapp app_name"
else
	$(DC_RUN) "python manage.py startapp $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))"
endif
ca: createapp	

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"