# Finvero Technical Test

## Description
This project is a technical test for Finvero created by Guillermo Reyes.

## Used libaries
- FastAPI 0.108.0
- uvicorn 0.25.0
- PyJWT 2.8.0
- SQLAlchemy 2.0.25
- requests 2.31.0

## Deploy info
### 1. Install Virtual Environment
This command installs virtualenv, a tool to create isolated Python environments.
```
pip install virtualenv
```

### 2. Create Virtual Environment
Creates a new virtual environment named venv using Python 3. This environment will isolate dependencies for your project.
```
python3 -m venv venv
```

### 2.5 Pip freeze
Create a requirements.txt only with local libraries.
```
pip freeze --local > requirements.txt
```

### 3. Set Environment Variables
The basic syntax to define an environment variable is as follows:
```
export DOCS_URL=/docs
export REDOC_URL=/redoc

export MYSQL_USER=admin
export MYSQL_PASS=password
export MYSQL_HOST=localhost
export MYSQL_PORT=3306
export DB_NAME=finvero
export DB_POOL_RECYCLE=3600
export DB_ECHO=False

export SECRET_KEY=develop
export ALGORITHM=HS256
export EXPIRE=60

export BELVO_URL_BASE=https://sandbox.belvo.com
export BELVO_TOKEN=[TOKEN_SANDBOX]
```

### 4. Install Dependencies
Installs project dependencies listed in the requirements.txt file. The --no-cache-dir flag prevents the use of cached packages.
```
pip install --no-cache-dir -r requirements.txt
```

### 5. Run FastAPI using Uvicorn
Starts the FastAPI application using Uvicorn. The --reload flag enables auto-reloading on code changes, and the --port 8001 specifies the port number.
```
uvicorn main:app --reload --port 8001
```

### 6. Build Docker Image
Builds a Docker image for the project and tags it as back-finverio.
```
docker build -t back-finverio .
```

### 7. Run Docker Container
Runs a Docker container in detached mode (-d), maps port 8001 on the host to port 8000 in the container, and names the container back-finverio.
```
docker run -d -p 8001:8000 --name back-finverio back-finverio
```

### 8. Run Docker Compose
Uses Docker Compose to start services defined in the docker-compose.yml file in detached mode (-d).
```
docker-compose up -d
```

### 9. URL to use

BaseAPI
http://0.0.0.0:8001/

Documentation (Swagger)
http://0.0.0.0:8001/docs


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

### 4. /v1/user_transactions
- Description: Endpoint to get a list of user transactions.
- Method: GET
- Requires a valid JWT token as a Bearer token in the Authorization header and an adecuated role (admin)..
- Response:
  - Returns a list of transactions.
- cURL
    ```
    curl --location 'http://localhost:8001/v1/user_transactions?page=[page_number]&user=[user_id]' \
    --header 'accept: application/json' \
    --header 'Authorization: Bearer [TOKEN]'
    ```

### 5. /v1/user_group_transactions
- Description: Endpoint to get a list of user transactions grouped by categories.
- Method: GET
- Requires a valid JWT token as a Bearer token in the Authorization header and an adecuated role (admin)..
- Response:
  - Returns a list of transactions.
- cURL
    ```
    curl --location 'http://localhost:8001/v1/user_group_transactions?page=[page_number]&user=[user_id]' \
    --header 'accept: application/json' \
    --header 'Authorization: Bearer [TOKEN]'
    ```

### 6. /v1/user_financial_health
- Description: Endpoint to obtain information about the user's financial health.
- Method: GET
- Requires a valid JWT token as a Bearer token in the Authorization header and an adecuated role (admin)..
- Response:
  - Returns a list of transactions.
- cURL
    ```
    curl --location 'http://localhost:8001/v1/user_financial_health?page=[page_number]&user=[user_id]' \
    --header 'accept: application/json' \
    --header 'Authorization: Bearer [TOKEN]'
    ```

### 7. /v1/user_income_expenses
- Description: Endpoint to obtain information about the income and expenses of each account.
- Method: GET
- Requires a valid JWT token as a Bearer token in the Authorization header and an adecuated role (admin)..
- Response:
  - Returns a list of transactions.
- cURL
    ```
    curl --location 'http://localhost:8001/v1/user_income_expenses?page=[page_number]&user=[user_id]' \
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
- belvo_endpoints.py
- users_roles.py
- users.py

### /routes/v1/
- login.py (Endpoint to obtain JWT token [email, password])
- register.py (Endpoint to add more users, requires Bearer token)

### /routes/v1/belvo/ (requires Bearer token)
- user_list.py (Endpoint to get a list of users from BELVO)
- user_transactions.py (Endpoint to get a list from transactions)
- user_group_transactions.py (Endpoint to get transactions grouped)
- user_financial_health.py (Endpoint to get information about user's financial health)
- user_financial_income_expenses.py (Endpoint to get information about incomes and expenses)