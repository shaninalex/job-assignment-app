start:
	docker compose -f ./docker-compose.dev.yml up -d --build

down_v:
	docker compose -f ./docker-compose.dev.yml down -v

stop:
	docker compose -f ./docker-compose.dev.yml stop