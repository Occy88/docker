include makefiles/color.mk
.PHONY: migrate migrate-head
_DB_PREFIX =$(DB_PREFIX)


migrate:
	$(_DB_PREFIX) "alembic revision --autogenerate -m migration && echo 'hi man'"
	$(_DB_PREFIX) "alembic upgrade head"
migrate-head:
	$(_DB_PREFIX) "alembic upgrade head"
