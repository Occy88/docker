SHELL = /bin/sh
# ENV defaults to local (so that requirements/local.txt are installed), but can be overridden
#  (e.g. ENV=production make setup).
ENV ?= local
# PYTHON specifies the python binary to use when creating virtualenv
PYTHON ?= python3.9

# Editor can be defined globally but defaults to nano
EDITOR ?= nano

# By default we open the editor after copying settings, but can be overridden
#  (e.g. EDIT_SETTINGS=no make settings).
EDIT_SETTINGS ?= yes

# Get root dir and project dir
PROJECT_ROOT ?= $(PWD)
SITE_ROOT 	 ?= $(PROJECT_ROOT)

DOCKER_COMPOSE			= docker-compose
DOCKER_RUN		= $(DOCKER_COMPOSE) run --rm
DOCKER_RUN_C	= $(DOCKER_RUN) octo_web
DOCKER_RUN_PYTHON = $(DOCKER_RUN_C) /usr/local/bin/python3
DOCKER_RUN_MANAGE = $(DOCKER_RUN_PYTHON) manage.py
TEST_PREFIX = $(DOCKER_RUN_PYTHON) -m
DB_PREFIX =  $(DOCKER_RUN_C) "/usr/local/bin/python3 -m "
.PHONY: setup


setup: validate-system-packages dir_setup
	@echo "$(INFO)Rebuilding docker$(COFF)"
	$(DOCKER_COMPOSE) down -v

ifeq ($(shell uname -s),Darwin)
	@echo "Running on macOS, skipping USER_ID and GROUP_ID setting"
	$(DOCKER_COMPOSE) build --build-arg POETRY_GROUPS=test
else
	@echo "Not running on macOS, setting USER_ID and GROUP_ID"
	$(DOCKER_COMPOSE) build $(cmd) --build-arg USER_ID=$(shell id -u) --build-arg GROUP_ID=$(shell id -g) --build-arg POETRY_GROUPS=test
endif
	$(DOCKER_COMPOSE) up -d
	make migrate
	@echo "$(FORMAT)\n\n=============[$(BOLD)$(SUCCESS) SETUP SUCCEEDED $(FORMAT)]========================="
	@echo "$(INFO) Run 'make run cmd=< -d >' to start Django development server.$(COFF)"


include makefiles/*.mk
