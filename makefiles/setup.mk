validate-system-packages:
	@echo "$(INFO)Validating system packages...$(COFF)"
	@#which poetry > /dev/null			|| (echo "$(ERROR)Poetry not found. Please install it.$(COFF)" && exit 1)
	@#which rabbitmqctl > /dev/null		|| (echo "$(ERROR)RabbitMQ command line tool not found. Please install it.$(COFF)" && exit 1)
	@which docker > /dev/null			|| (echo "$(ERROR)Docker not found. Please install it.$(COFF)" && exit 1)
	@#which docker-compose > /dev/null 	|| (echo "$(ERROR)Docker Compose not found. Please install it.$(COFF)" && exit 1)
	@echo "All required system packages are installed."

.env: .env-dev-example
	@if [ ! -f .env ]; then \
		echo "$(CYAN)Creating .env file$(COFF)"; \
		install -b --suffix=.bak -m 644 .env-dev-example .env; \
	else \
		echo "$(CYAN).env file already exists$(COFF)"; \
	fi
merge-env:
	if [ -z "$(file2)" ]; then \
		cp $(file1) .env; \
	else \
		cat $(file1) $(file2)  > .env; \
	fi

print_make_state:
	echo "Current ENV_FILES: $(ENV_FILES)"
dir_setup: .env
# Set environment commands

set-integration:
	$(MAKE) merge-env file1=.env.development file2=.env.integration

set-development:
	$(MAKE) merge-env file1=.env.development

