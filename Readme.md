# Finvero Technical Test

## Description
This project is a technical test for Finvero created by Guillermo Reyes.

## Used libaries
- FastAPI 0.108.0
- uvicorn 0.25.0
- PyJWT 2.8.0
- SQLAlchemy 2.0.25
- requests 2.31.0

## Endpoints

### 1. /v1/login
- Description: Endpoint for user login.
- Method: POST
- Request:
  - Parameters:
    - email: User email
    - password: User password
- Response:
  - Returns a JWT token if the login is successful.
- cURL
    ```
    curl --location 'http://localhost:8001/v1/login' \
    --header 'accept: application/json' \
    --header 'Content-Type: application/x-www-form-urlencoded' \
    --data-urlencode 'username=email@email.com' \
    --data-urlencode 'password=password'
    ```

### 2. /v1/register
- Description: Endpoint for user registration.
- Method: POST
- Request:
  - Parameters:
    - email: User email
    - password: User password
    - name: User name
    - lastname: User lastname
    - role_id: User role id
  - Requires a valid JWT token as a Bearer token in the Authorization header and an adecuated role (admin).
- Response:
  - Returns information about the registered user.
- cURL
    ```
    curl --location 'http://localhost:8001/v1/register/' \
    --header 'accept: application/json' \
    --header 'Authorization: Bearer [TOKEN]' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "email": "email@email.com",
        "password": "passwortd",
        "name": "John",
        "lastname": "Smith",
        "role_id": 1
    }'
    ```

### 3. /v1/user_list
- Description: Endpoint to get a list of users.
- Method: GET
- Requires a valid JWT token as a Bearer token in the Authorization header and an adecuated role (admin)..
- Response:
  - Returns a list of users.
- cURL
    ```
    curl --location 'http://localhost:8001/v1/user_list?page=1' \
    --header 'accept: application/json' \
    --header 'Authorization: Bearer [TOKEN]'
    ```

## Default Environment Variables

### FASTAPI DOCS
```
DOCS_URL = /docs
REDOC_URL = /redoc
```

### DATABASE CONFIG
```
MYSQL_USER = admin
MYSQL_PASS = password
MYSQL_HOST = localhost
MYSQL_PORT = 3306
DB_NAME = finvero
DB_POOL_RECYCLE = 3600
DB_ECHO = False
```

### JWT CONFIG
```
SECRET_KEY = develop
ALGORITHM = HS256
EXPIRE = 60
```

### BELVO CONFIG
```
BELVO_URL_BASE = https://sandbox.belvo.com
BELVO_TOKEN = [TOKEN_SANDBOX]
```

## Project Structure
### /
- .gitignore
- docker-compose.yml (Includes Python + MySQL containers)
- Dockerfile
- main.py (FastAPI)
- requirements.txt

### /config/
- belvo.py (Integration with BELVO API)
- mysql.py (Singleton connection with the database)
- passwords.py (Password encryption)
- tokens (PyJWT)

### /models/
- users_roles
- users

### /routes/v1/
- login.py (Endpoint to obtain JWT token [email, password])
- register.py (Endpoint to add more users, requires Bearer token)

### /routes/v1/belvo/
- user_list.py (Endpoint to get a list of users from BELVO, requires Bearer token)
