# FastAPI-Financial

A FastAPI project for managing financial data from Belvo's API. 
The list of specifications is in the [Technical Test](.github/fordevs/TechnicalTest.md) file.

| [Installation](#installation)
| [InstallDocker](#installation-docker)
| [DesignPattern](#design-pattern)
| [ForDevelopers](#fordevelopers)
| [ProjectActionPlan](#project-action-plan)
| [ExtraTools](#extratools) |

## Installation

The project will be developed with the nexts versions:
+ Python 3.10
+ MySQL 8.0

Create a virtual environment
```bash
python3 -m venv env
```

Activate the virtual environment
```bash
source env/bin/activate
```

Install the requirements
```bash
pip install -r requirements.txt
```

Create the database in MySQL
```bash
mysql -u root -p
```

Inside of execute the sql:
```sql
CREATE DATABASE fastapi_financial;
```

Create the file .env

+ Now! Stop! We need copy the file .env.example and rename to .env,
and add change the values of variables correspondents to the credentials,
for more information check the [File of Variables](#file-of-variables).

Run the project
```bash
uvicorn src.main:app --reload
```

<br>

## Installation Docker

If you want to run the project with Docker, you need to install Docker and
Docker Compose, and follow the nexts steps:

Update the db url in the `.env` file
```bash
DATABASE_URL_SANDBOX='mysql+pymysql://root:root@db:3306/fastapi_financial'
```

Build the image
```bash
docker-compose build
```

Run the project in background
```bash
docker-compose up -d
```

Enter to the container
```bash
docker-compose exec api bash
```

Status of containers
```bash
docker-compose ps
```

Restart the project
```bash
docker-compose restart
```

Stop the project
```bash
docker-compose down
```

<br>

## ForDevelopers

For follow and respect a code style, will be used the nexts tools:

+ Linter

The linter will be used for check the code style and syntax errors. 
With the [pre-commit](https://pre-commit.com/) and 
[flake8](https://flake8.pycqa.org/en/latest/).

Execute the command for lint the code
```bash
pre-commit run --all-files
```

+ Testing

The tests will be used for check the code logic and errors.
With [pytest](https://docs.pytest.org/) create the unit and 
integration features tests.

Execute the command for run the tests
```bash
pytest
```

### File of Variables
In this file `.env`, we will define the variables of credentials, and 
we can change from environment to environment. Obviously, is private!

#### Fundamentals Global Variables
+ APP_ENV = Define the environment of project (sandbox, dev, prod).
+ PATH_CONFIG_YAML = Default 'src/core/config.yaml'. Change if you need.

#### Fundamentals Environment Variables
+ DOMAIN = Define the domain of project. (Default: '127.0.0.1').
+ DATABASE_URL = Define the url of database. (Default: MySQL).
+ BELVO_URL = Define the url of Belvo API. (Defaults are configured).
+ BELVO_SECRET_ID = Generate in 
[Belvo's APIs Dashboard](https://dashboard.belvo.com/sandbox/api-keys/).
+ BELVO_SECRET_PASSWORD = Generate in 
[Belvo's APIs Dashboard](https://dashboard.belvo.com/sandbox/api-keys/).

<br>

## Design Pattern
The project will be developed with the design pattern of units of work,
and the architecture will divide into the nexts three 'layers':

### Presentation Layer
Manage the interactions with the user (or client system) through the API.
Here, the routes and endpoints are defined. Handles requests and responses.
+ `src/api/`    | Structure of API, init and global configs.
+ `src/api/v1/` | Manage the routes and endpoints of API.

### Business Logic Layer
Manage the business logic of the application, and the validation of input 
and output data. Here, the ORM models are defined.
+ `src/models/` | Contains the ORM models, represent the database relations.
+ `src/schemas/`| Define the schemas for validate the input and output data.

### Data Access Layer
Manage the database connections and transactions. Here, the configuration
and sessions are defined. Following the ACID properties.
+ `src/core/database.py` | Gest the database connection and sessions.

### Others Inside Features
+ `src/core/auth.py`    | Auth JWT for API.
+ `src/core/config.py`  | Config and Variables.
+ `src/utils/util_any`  | Auxiliary functions.    
+ `tests/test_any`      | Unit and Integration Tests.
+ `respones_schems.py`  | Standard custom responses.

<br>

## Project Action Plan

A list of tasks to complete the project.

### Preliminaries
- [X] ~~Create a GitHub repository.~~
- [X] ~~Create and register credentials for Belvo.~~
- [ ] Read, understand, and implement Belvo's documentation.
- [X] ~~Take notes from Belvo's documentation.~~

### Project Architecture and Patterns Definition
- [X] ~~Define the project's architecture and patterns.~~
- [X] ~~META Create a project action plan META.~~

### Project Structure
- [ ] Create project structure: 
    + ~~`src` and `tests`.~~
    + follow the pattern design
    + respect the architecture
- [X] ~~Initialize a project with FastAPI.~~
- [X] ~~Create a Dockerfile for Python.~~
- [X] ~~Create a docker-compose file.~~
- [X] ~~Add a MySQL database (optional) in docker-compose.~~

### Management of Credentials and Environment Variables
- [X] ~~Create logic to handle credentials.~~
- [X] ~~Create logic to handle environment variables.~~
    + ~~Test use of three environments (from Belvo's docs)~~
- [X] ~~Docs for manage credentials in repository.~~

### Development and Code Quality Tools
- [X] ~~Add a linter (pre-commit and flake8).~~
- [X] ~~Add pytest for local testing.~~

### Continuous Integration and Deployment
- [X] ~~Configure linter in GitHub Actions.~~
- [X] ~~Configure pytest in GitHub Actions.~~
- [X] ~~Consider automatic deployment configuration in GitHub Actions.~~

### API and Database Development
- [ ] Design database models for users, transactions, and categories.
- [ ] Implement authentication and session management.
- [ ] Develop endpoints for transaction lists, user listings, etc.
- [ ] Integrate and test the connection with Belvo's API.
- [ ] Implement logic for financial analysis (income and expenses).

### Optimization and Error Handling
- [ ] Optimize database queries for high performance.
- [ ] Implement robust and consistent error handling.

### Testing and Validation
- [ ] Develop unit and integration tests.
- [ ] Validate input and output data in the API.

### Final Evaluation and Improvements
- [ ] Review code scalability and readability.
- [ ] Perform final tests of the complete application.
- [ ] Refine and improve based on feedback or test results.

### Project Documentation
- [ ] Document all development steps and project configurations.
- [ ] Include usage guides and local deployment in the README.

### Deployment and Delivery
- [X] ~~Clone project in server.~~
- [X] ~~Configure server for production.~~
- [X] ~~Create service linux for project.~~
- [X] ~~Configure gunicorn for project.~~
- [X] ~~Create subdomain and configure DNS.~~
- [X] ~~Configure nginx like reverse proxy.~~
- [X] ~~Configure SSL certificate (certbot).~~
- [ ] Test and validate finished project.

<br>

## ExtraTools
Tree of Project
```bash
tree -I "env|.git|.pytest_cache|__pycache__|.coverage" -la
```

For more information about Belvo API, can read 
the [Belvo's Docs](.github/fordevs/BelvoDocs.md).

Thanks for this great full implementation of 
[Python API Belvo](https://github.com/belvo-finance/belvo-python)
all `/belvo/` code its a copy of this repository. 

### END!
