# AlkohoLove-backend-service

## Installing dependencies

Use `$ pip install -r requirements.txt`

## Local development

When running with IDE, set Run/Debug configurations with env variable  
`DATABASE_URL=postgresql+asyncpg://alkoholove_admin:Test1234@localhost:5432/alkoholove`  
When using docs to test the API use `ModHeader` extension and add header `Authorization: Bearer <token>`

## Docs
Docs are available under `/docs` path

## Docker

To run `$ docker-compose up --build -d`  
To stop `$ docker-compose down --volumes`  
To run just the db `$ docker-compose run -d --service-ports db`  
Db is persisted between launches, to get a brand-new db delete `postgres-data` directory  
Backend on docker will be under `http://localhost:8008/docs`

## Tests

**Docker container with the database must be running!**  
Set environment variable `DATABASE_URL=postgresql+asyncpg://alkoholove_admin:Test1234@localhost:5432/alkoholove`  
To run tests use `$ pytest` command in root directory

## Linters

To run linter check use `$ pycodestyle ./src --source-code` in root directory or  
`$ pycodestyle . --source-code` in src directory

## COMMITS CONVENTION

Commits merged into master should follow conventional 
commits [convention](https://gist.github.com/Zekfad/f51cb06ac76e2457f11c80ed705c95a3).
Long story short: `<type>: <message> [<jira-ticket>]`
