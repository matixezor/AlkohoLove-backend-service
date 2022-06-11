# AlkohoLove-backend-service

## Installing dependencies

Use `$ pip install -r requirements.txt`

## Local development

When running with IDE, set Run/Debug configurations with env variable  
`DATABASE_URL=mongodb://alkoholove_admin:Test1234@localhost:27017/alkoholove?retryWrites=true&w=majority`  
`CLOUDINARY_URL` - get from heroku  
To upload image to production storage add env variable `ALCOHOL_IMAGES_DIR=alcohols`  
When using docs to test the API use `ModHeader` extension and add header `Authorization: Bearer <token>`

## Docs

Docs are available under `/docs` path

## Docker

To run `$ docker-compose up --build -d`  
To stop `$ docker-compose down --volumes`  
To run just the db `$ docker-compose run -d --service-ports mongodb`  
Db is persisted between launches, to get a brand-new db delete `mongo-data` directory  
Backend on docker will be under `http://localhost:8008/docs`  
To run with image handling add env variable to `Dockerfile` `ENV CLOUDINARY_URL <get from heroku>`  
To upload image to production storage add env variable to `Dockerfile` `ENV ALCOHOL_IMAGES_DIR alcohols`  

## Tests

To run tests use `$ pytest` command in tests directory

## Linters

To run linter check use `$ pycodestyle ./src --source-code` in root directory or  
`$ pycodestyle . --source-code` in src directory

## COMMITS CONVENTION

Commits merged into master should follow conventional
commits [convention](https://gist.github.com/Zekfad/f51cb06ac76e2457f11c80ed705c95a3). Long story
short: `<type>: <message> [<jira-ticket>]`
