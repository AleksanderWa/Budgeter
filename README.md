# Family Budget project
Made with **Python 3.10** and **Django 4.0**

Pure backend application, serving REST API. For managing budgets.

### Main features:
- Register user
- Every user can create any numbers of budgets
- Each budget can have more than 1 owner
- Create records (income, expense) for given budget
- Delete budget / records
- Update budget / records
- Pagination for each endpoint set to 20 results
- seed_db command to create fixtures


- All key features beside user registration are protected. User needs to log in to acquire token which should be added to AUTHORIZATION header of each request when performing any of the action listed above. [Examples](#example-requests)

## URLS:
- [GET, POST] /budgets
- [GET, PATCH, DELETE] /budgets/<pk>
- [GET, POST] /records
- [GET, PATCH, DELETE] /records/<pk>
- [POST] /account/register
- [POST] /api-token-auth

## Installation

**Simple download adn run:**
Make sure docker and docker compose are installed

1. git clone project
2. navigate to the main app directory
3. run script build_n_run.sh
   - build and run application inside container
   - database migrations
   - seed db

For Windows users there might be need for using winpty to run commands from build_n_run.sh
- before each command inside build_n_run.sh put "winpty" keyword, eg. winpty docker-compose up --build -d

### seed_db command:
- this will create:
  - 2 users (Batman, Star Lord)
  - 3 budgets
  - 10 budget records

When application is up and running and database is seeded with fixtures you can finally consume API
## Example requests
### Send POST request to acquire token for user Batman:

`curl --location --request POST '127.0.0.1:8000/api-token-auth/' --header 'Content-Type: application/json' --data-raw '{"username": "Batman", "password": "password"}'`

### GET user's budgets:
`curl --location --request GET '127.0.0.1:8000/budgets/' \
--header 'Authorization: Token 37abb4b91345b0baa13bfdaa7cf3955b0bd67ccd'`

### GET user's records with category id = 1 or id = 2
`curl --location --request GET '127.0.0.1:8000/records/?category=1&category=2' \
--header 'Authorization: Token a833ff9d8576ce151079c364b43a7712480a0854' \`

You should get list of budgets - records and categories. Using Postman it should look like that:
![img.png](img.png)

### Create budget with records example:
`curl --location --request POST '127.0.0.1:8000/budgets/' \
--header 'Authorization: Token 37abb4b91345b0baa13bfdaa7cf3955b0bd67ccd' \
--header 'Content-Type: application/json' \
--data-raw '{
            "name": "Family budget",
            "owners": [1],
            "records": [{"amount": "25.05"}, {"amount": "-20.12"}, {"amount": "15.00"}, {"amount": "-20.21"}]
        }'`

## For developers
Read this if you are software developer and want to run this project on your machine without using docker:
1. git clone the project
2. create postgres database and change project django settings accordingly to use your database
3. ideally create virtual env and install requirements from requirements.txt file

### When application is up and running:
- Run django command: python manage.py seed_db to populate database


## Tests
There are 34 views tests located in budget module.

To run tests simply execute following command:
### Docker version:
- docker-compose exec web python ./manage.py test --keepdb
### Local version:
- python manage.py test --keepdb
