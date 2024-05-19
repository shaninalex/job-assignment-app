# Example backend

```bash
# run in docker
docker compose -f docker-compose.dev.yml up -d --build

# login into api container
docker compose -f docker-compose.dev.yml exec -it api sh

# create admin account
python3 cli.py --create-admin
```

Then create some example positions.
