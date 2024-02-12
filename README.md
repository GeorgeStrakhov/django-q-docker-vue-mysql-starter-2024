## Run locally

1. clone the repo
2. create .env file in the root (see env.example)
3. `docker-compose up`

## Run prod
(assuming ubuntu server with Docker and docker-compose ready and configured)

- first, `touch acme.json`
- then `chmod 600 acme.json`
- setup .env with correct details
- `docker-compose -f docker-compose.prod.yml up -d`

## What's inside

- traefik for reverse proxy and https management
- backend: django with djangorestframework exposed on /api
- queue: django-q2 for long task queue
- redis: for task que management
- frontend: vue3 with vite
- db: mysql
- db: adminer available on :8080 during dev
- for ease of development: code attached as separate volumes. hotreload enabled both front and back
- all env variables are in the top level .env file and then exposed to each container via docker-compose environment instructions

*NB!* when installing packages for front or back - if you don't want to rebuild the dockerfile, then just `docker-exec` into a running container and `yarn add` or `pip install` from there

## TODO

- catch a weird corner case bug that password reset sometimes gives a refresh token error if previously logged in (solved by page reload)
- implement user settings page
- implement stripe payments and plans
- test deployments
