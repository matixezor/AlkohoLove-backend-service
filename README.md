# AlkohoLove-service

## Installing dependencies

Use `pip install -r requirements.txt`

## Running docker

Use `docker-compose up --build -d`  
Db `jdbc:postgresql://localhost:5432/alkoholove`

## Docs

`http://localhost:8008/docs`

## Tests

To run tests use `$ pytest` command in root directory

## Linters

To run linter check use `$ pycodestyle ./src --source-code` in root directory 
or `$ pycodestyle . --source-code` in src directory

## COMMITS CONVENTION

Commits merged into master should follow conventional 
commits [convention](https://gist.github.com/Zekfad/f51cb06ac76e2457f11c80ed705c95a3).
Long story short: `<type>: <message> [<jira-ticke>]`
