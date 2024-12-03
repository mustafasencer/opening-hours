.PHONY: dev-deps deps format lint run docker-build docker-run test test-with-coverage help
.DEFAULT_GOAL := help

SERVICE=opening-hours
IMAGE?=$(SERVICE):latest
PORT=8000

## dev-deps: Install python dev packages
dev-deps:
	pip install -r requirements.dev.txt

## deps: Install python packages
deps:
	pip install -r requirements.txt

## format: Format codebase
format:
	autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place app tests --exclude=__init__.py
	black app tests
	isort app tests --profile black

## lint: Lint codebase
lint:
	mypy app
	black app tests --check
	isort app tests --check-only --profile black

## run: Run service
run:
	uvicorn app.main:app --reload

## docker-build: Docker build
docker-build:
	docker build -t $(IMAGE) .

## docker-run: Docker run service
docker-run:
	docker run -d --name $(SERVICE) -p $(PORT):$(PORT) $(IMAGE)

## test: Run the project unit tests
test:
	pytest -v

## test-with-coverage: Run the unit tests and calculate the coverage
test-with-coverage:
	pytest --cov-report term-missing --cov=.

## :
## help: Print out available make targets.
help: Makefile
	@echo
	@echo " Choose a command run:"
	@echo
	@sed -n 's/^##//p' $< | column -t -s ':' |  sed -e 's/^/ /'
	@echo
