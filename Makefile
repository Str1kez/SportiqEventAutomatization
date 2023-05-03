.PHONY: build
.SILENT:

args := $(wordlist 2, 100, $(MAKECMDGOALS))

worker:
	poetry run dramatiq app.__main__ -p 3

run:
	poetry run python3 -m app

build:
	docker build . -t event-auto -f build/service/Dockerfile

up:
	docker compose up -d --remove-orphans

down:
	docker compose down
