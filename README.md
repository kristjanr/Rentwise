# YBuy p2p renting app

A Django 1.10 based web app built with Python 3.6, using Postgresql database using the [Heroku Django Template](https://github.com/heroku/heroku-django-template)
Built for running on Heroku.

## Local setup on OSX
* Install postgres database. Currently, Heroku uses 9.3.15 but the development has been successfully done with 9.6.1.0, so both are fine
* Copy .env_default file as .env and add the correct environment variables
* Set the environment variables: `source .env`
* `pip install -r requirements.txt`
* `python manage.py collectstatic`
    
## Running tests

`python manage.py test`

## Running server

`python manage.py runserver`

## Deploy

* `git push heroku master`
* Check that you have all the needed environment variables at [Heroku](https://dashboard.heroku.com/apps/rentwise/settings)
* If migrations were added, then run migrate on heroku: `heroku run python manage.py migrate`
