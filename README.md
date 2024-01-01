# FastAPI-Financial

A FastAPI project for managing financial data from Belvo's API. 
The list of specifications is in the [Technical Test](.github/fordevs/TechnicalTest.md) file.

| [Installation](#installation)
| [ProjectActionPlan](#project-action-plan)
| [ExtraTools](#extratools) |

## Installation
TODO!

<br>

## Project Action Plan

A list of tasks to complete the project.

### Preliminaries
- [X] ~~Create a GitHub repository.~~
- [X] ~~Create and register credentials for Belvo.~~
- [ ] Read, understand, and implement Belvo's documentation.
- [ ] Take notes from Belvo's documentation.

### Project Architecture and Patterns Definition
- [ ] Define the project's architecture and patterns.

### Project Structure
- [ ] Create project structure: 
    + `src` and `tests`.
    + follow the pattern design
    + respect the architecture
- [ ] Initialize a project with FastAPI.
- [ ] Create a Dockerfile for Python.
- [ ] Create a docker-compose file.
- *[ ] Add a MySQL database (optional) in docker-compose.*

### Management of Credentials and Environment Variables
- [ ] Create logic to handle credentials.
- [ ] Create logic to handle environment variables.
    + Test use of three environments (from Belvo's docs)
- [ ] Docs for manage credentials in repository.

### Development and Code Quality Tools
- [ ] Add a linter (pre-commit and flake8).
- [ ] Add pytest for local testing.

### Continuous Integration and Deployment
- [ ] Configure linter in GitHub Actions.
- [ ] Configure pytest in GitHub Actions.
- [ ] Consider automatic deployment configuration in GitHub Actions.

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
- [ ] Clone project in server.
- [ ] Configure server for production.
- [ ] Create service linux for project.
- [ ] Configure gunicorn for project.
- [ ] Create subdomain and configure DNS.
- [ ] Configure nginx like reverse proxy.
- [ ] Configure SSL certificate (certbot).
- [ ] Test and validate finished project.

<br>

## ExtraTools
Tree of Project
```bash
tree -I "env|.git|.pytest_cache|__pycache__" -la
```

For more information about Belvo API, can read the [Belvo's Docs](.github/fordevs/BelvoDocs.md).

### END!