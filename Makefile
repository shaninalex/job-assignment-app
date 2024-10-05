start:
	docker compose -f ./docker-compose.dev.yml up -d --build

down_v:
	docker compose -f ./docker-compose.dev.yml down -v

stop:
	docker compose -f ./docker-compose.dev.yml stop


test_start:
	docker compose -f ./docker-compose.test.yml up -d --build

test_down_v:
	docker compose -f ./docker-compose.test.yml down -v

test_stop:
	docker compose -f ./docker-compose.test.yml stop