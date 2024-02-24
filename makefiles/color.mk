SHELL = /bin/sh

BLACK	?= \033[0;30m
RED		?= \033[0;31m
GREEN	?= \033[0;32m
LIGHT_GREEN ?= \033[1;32m
YELLOW	?= \033[0;33m
BLUE	?= \033[0;34m
LIGHT_BLUE ?= \033[1;36m
PURPLE	?= \033[0;35m
CYAN	?= \033[0;36m
GRAY	?= \033[0;37m
COFF	?= \033[0m

info 	?= $(tput 1)
SUCCESS ?= $(LIGHT_GREEN)
WARNING ?= $(YELLOW)
ERROR 	?= $(RED)
DEBUG 	?= $(CYAN)
FORMAT 	?= $(GRAY)
BOLD ?= \033[1m
