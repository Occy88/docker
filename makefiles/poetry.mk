#include makefiles/main.mk
include makefiles/color.mk
.PHONY: pre pre-commit test psql coverage profile show-profile
_TEST_PREFIX = $(TEST_PREFIX) poetry run

test:
	$(_TEST_PREFIX) poetry run pytest --durations=50 --disable-warnings $(args) $(path); RESULT=$$? ;

coverage:
	@echo "$(INFO)Running automatic code coverage check$(COFF)"
	$(_TEST_PREFIX) coverage run -m py.test
	$(_TEST_PREFIX) coverage html
	$(_TEST_PREFIX) coverage report

pre: pre-commit
pre-commit:
	@echo "$(INFO)Running pre-commit routine$(COFF)"
	make schema
	poetry run pre-commit run --all-files


profile: clean
	docker-compose down
	@echo "$(INFO)Running automatic tests$(COFF)"
	make run cmd=-d
	$(DOCKER_COMPOSE_DJANGO) py.test --durations=30 --disable-warnings $(args) $(path) --profile; RESULT=$$? ;
	$(DOCKER_COMPOSE_DJANGO) rm -rf django_extras/migrations

show-profile:
	poetry run snakeviz prof/combined.prof