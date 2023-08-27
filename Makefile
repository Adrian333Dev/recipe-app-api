# Makefile

# Docker Compose commands
DC=docker-compose
DC_BUILD=$(DC) build
DC_UP=$(DC) up
DC_DOWN=$(DC) down
DC_RUN=$(DC) run --rm app sh -c
FLAKE8=$(DC_RUN) "flake8"
STARTPROJECT=$(DC_RUN) django-admin startproject


default: help

dc:
ifeq ($(filter $(MAKECMDGOALS),b),b)
	$(DC_BUILD) 
else ifeq ($(filter $(MAKECMDGOALS),u),u)
	$(DC_UP)
else ifeq ($(filter $(MAKECMDGOALS),d),d)
	$(DC_DOWN)
else ifeq ($(filter $(MAKECMDGOALS),r),r)
	$(DC_RUN) $(filter-out $@,$(MAKECMDGOALS))
else
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  b            Build docker image"
	@echo "  u            Run docker container"
	@echo "  d            Stop docker container"
endif

flake8:
	$(FLAKE8)
f8: flake8

createproject:
ifeq ($(filter-out $@,$(MAKECMDGOALS)),)
	@echo "Usage: make createproject project_name [optional: .]"
else
	$(DC_RUN) "django-admin startproject $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))"
endif
cp: createproject

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  dc					 Docker Compose commands (Usage: make [target] [args])"
	@echo "  flake8 (f8)			 Run flake8 in docker container"
	@echo "  startproject (sp)	 Create new Django project (Usage: make [target] [project_name])"
	@echo "  help					 Show this help message"