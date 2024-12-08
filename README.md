#  Casting Agency Project

## About
Welcome to the Casting Agency Project, a powerful API designed to streamline the management of actors and movies. This system enables casting professionals to efficiently add, modify, and view their database, ensuring secure access with Role-Based Access Control (RBAC).
## Getting Started

### Installing Dependencies

#### Python 3.7.0

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### PIP Dependencies

In the warranty-tracker directory, run the following to install all necessary dependencies:

```bash
pip install -r requirements.txt
```
This will install all of the required packages.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Running the server
To run the server, execute:
```
python -m flask run
```
We can now also open the application via Render using the URL:
https://fsnd-capstone-4vmj.onrender.com/

The live application can only be used to generate tokens via Auth0, the endpoints have to be tested using curl or Postman 
using the token since I did not build a frontend for the application.

## DATA MODELING:
#### models.py
The schema for the database and helper methods to simplify API behavior are in models.py:
- There are three tables created: Movies, Actor
- The Actor table has a foreign key on the User table for movie_id.
Each table has an insert, update, delete, and format helper functions.

## Roles and the permissions
@app.errorhandler decorators were used to format error responses as JSON objects. 
Custom @requires_auth decorator were used for Authorization based on roles of the user. 
Three roles are assigned to this API: 'Casting Assistant' and 'Casting Director' and 'Executive Producer'.
- Casting Assistant: 
    Can view actors and movies
- Casting Director
    All permissions a Casting Assistant has and…
    Add or delete an actor from the database
    Modify actors or movies
- Executive Producer
    All permissions a Casting Director has and…
    Add or delete a movie from the database

A token needs to be passed to each endpoint.
The token can be retrived by following these steps:
  - Go to: https://hieutt.us.auth0.com/authorize?audience=FSND_Image&response_type=token&client_id=atWrH86W0yNtXe8I4sGywMzzTn8DEGuM&redirect_uri=https://127.0.0.1:5000/login-results
  - Login to each account below to get the token for each role
# Role - Account(acc/pass):
  - Casting Assistant: trtrghieu@gmail.com - Lucario1231@
  - Casting Director: hieutt@gmail.com - Lucario1231@
  - Executive Producer: hieutt101020@gmail.com - Lucario1231@
  - Link to get token store in Auth.txt

### Endpoint for Actors/Movies include permissions associated for each request
  Project includes a custom @requires_auth decorator that:
  get the Authorization header from the request
  Decode and verify the JWT using the Auth0 secret
  take an argument to describe the action
  i.e. @require_auth(‘create:drink’)

  raise an error if:
    the token is expired
    the claims are invalid
    the token is invalid
    the JWT doesn’t contain the proper action

`GET '/movies'`
- @requires_auth('read:movies')
- Fetches a list of actors
- Request Arguments: None
- Returns: list of actors contain id, title, release_date

```json
{
  {
    "id": 1,
    "title": "Inception",
    "release_date": "2010-07-16"
  },
  {
    "id": 2,
    "title": "The Dark Knight",
    "release_date": "2008-07-18"
  },
  {
    "id": 3,
    "title": "Interstellar",
    "release_date": "2014-11-07"
  }
}
```

`GET/movies/<int:id>`
- @requires_auth('read:movies')
- Get a special movie by id
- Request Arguments: `id` - integer
- Returns: a movie object
``` json
{
  "id": 1,
  "title": "Inception",
  "release_date": "2024-07-16"
}
```

`POST/movies`
- @requires_auth('create:movies')
- This endpoint creates a new movie
- Request Body:
```json
{
    "title": "Dunkirk",
    "release_date": "2024-07-21"
},
```

- Returns: a single new movie object and message-status
```json
{
    {
        "title": "Dunkirk",
        "release_date": "2024-07-21"
    },
    "message": True
}
```

`PATCH/movies/<int:id>`
- @requires_auth('modify:movies')
- This endpoint updates the information of an existing movie by `id`
- Request Body:
```json
{
  "title": "Dunkirk (Updated)",
  "release_date": "2017-07-22"
}
```
- Returns: a single movie object after update and message-status
```json
{
    {
        "title": "Dunkirk",
        "release_date": "2024-07-21"
    },
    "message": True
}
```

`DELETE/movies/<int:id>`
- @requires_auth('delete:movies')
- This endpoint deletes a movie by `id`
- Request Arguments: `id` - integer
- Returns: a single movie object deleted and message-status
```json
{
    {
        "title": "Dunkirk",
        "release_date": "2024-07-21"
    },
    "message": True,
}
```

### Endpoint for /Actors

`GET '/actors'`
- @requires_auth('read:actors')
- Fetches a list of actors
- Request Arguments: None
- Returns: list of actors contain id, name, age, gender, movie_id, movie

```json
{
  "actors": [
    {
      "id": 1,
      "name": "Leonardo DiCaprio",
      "age": 45,
      "gender": "Male",
      "movie_id": "1",
      "movie": {
        "id": 1,
        "title": "Inception",
        "release_date": "2010-07-16"
      }
    },
    {
      "id": 2,
      "name": "Natalie Portman",
      "age": 39,
      "gender": "Female",
      "movie_id": "1",
      "movie": {
        "id": 2,
        "title": "Black Swan",
        "release_date": "2010-12-03"
      }
    }
  ]
}

```

`GET/actors/<int:id>`
- @requires_auth('read:actors')
- Get a special actor by id
- Request Arguments: `id` - integer
- Returns: a actor object
``` json
{
    "id": 2,
    "name": "Natalie Portman",
    "age": 39,
    "gender": "Female",
    "movie_id": "1",
    "movie": {
    "id": 2,
    "title": "Black Swan",
    "release_date": "2010-12-03"
    }
}
```

`POST/actors`
- @requires_auth('create:actors')
- This endpoint creates a new actor
- Request Body:
```json
{
  "name": "Brad Pitt",
  "age": 56,
  "gender": "Male",
  "movie_id": 1 
}
```

- Returns: a single new actor object and message-status
```json
{
    "message": true,
    "actor": {
        "id": 3,
        "name": "Brad Pitt",
        "age": 56,
        "gender": "Male",
        "movie": {
        "id": 1,
        "title": "Inception",
        "release_date": "2010-07-16"
        }
    }
}
```

`PATCH/actors/<int:id>`
- @requires_auth('modify:actors')
- This endpoint updates the information of an existing actor by `id`
- Request Body:
```json
{
  "name": "Leonardo DiCaprio (Updated)",
  "age": 46,
  "gender": "Male",
  "movie_id": 2
}

```
- Returns: a single actor object after update and message-status
```json
{
  "actor": {
    "id": 1,
    "name": "Leonardo DiCaprio (Updated)",
    "age": 46,
    "gender": "Male",
    "movie": {
      "id": 2,
      "title": "The Revenant",
      "release_date": "2015-12-25"
    }
  },
  "message": true
}
```

`DELETE/actor/<int:id>`
- @requires_auth('delete:actors')
- This endpoint deletes a actor by `id`
- Request Arguments: `id` - integer
- Returns: a single actor object deleted and message-status
```json
{
  "actor": {
    "id": 1,
    "name": "Leonardo DiCaprio (Updated)",
    "age": 46,
    "gender": "Male",
    "movie": {
      "id": 2,
      "title": "The Revenant",
      "release_date": "2015-12-25"
    }
  },
  "message": true
}
```
  # Testing
All unittests store in test_app.py. 
Include one test for expected success and error behavior for each endpoint using the unittest library.
Includes tests demonstrating role-based access control, two per role.

To run this file use:
```
dropdb FNSD_CAPSTONE_TEST
createdb FNSD_CAPSTONE_TEST
python unittest test_app.py
```  
The tests include one test for expected success and error behavior for each endpoint, and tests demonstrating role-based access control, 
where all endpoints are tested with and without the correct authorization.
Further, the file 'warranty-tracker-test-endpoints.postman_collection.json' contains postman tests containing tokens for specific roles.
To run this file, follow the steps:
1. Go to postman application.
2. Load the collection --> Import -> directory/FSND CAPSTONE.postman_collection.json
3. Click on the runner, select the collection and run all the tests.

## THIRD-PARTY AUTHENTICATION
#### auth.py
Auth0 is set up and running. The following configurations are in a .env file which is exported by the app:
- The Auth0 Domain Name
- The JWT code signing secret
- The Auth0 Client ID
The JWT token contains the permissions for the 'Casting Assistant' and 'Casting Director' and 'Executive Producer'.

## DEPLOYMENT
The app is hosted live on heroku at the URL: 
https://fsnd-capstone-4vmj.onrender.com/

However, there is no frontend for this app yet, and it can only be presently used to authenticate using Auth0 by entering
credentials and retrieving a fresh token to use with curl or postman.
