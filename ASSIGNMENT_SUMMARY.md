# DevOps Assignment Summary

## Project Overview

- **Application**: User Management System (Flask + SQLite)
- **CI/CD**: Jenkins Pipeline with automated testing
- **Containerization**: Docker deployment
- **Testing**: pytest (unit) + Selenium (integration)

## Key Files

1. `app.py` - Flask web application
2. `Jenkinsfile` - Complete CI/CD pipeline
3. `test_unit.py` - Unit tests (pytest)
4. `test_selenium.py` - Selenium tests (4 test cases)
5. `Dockerfile` - Container configuration
6. `requirements.txt` - Python dependencies

## Jenkins Pipeline Stages

1. **Code Linting** - flake8 quality checks
2. **Code Build** - Install dependencies
3. **Unit Testing** - pytest execution
4. **Containerized Deployment** - Docker build & run
5. **Selenium Testing** - Automated browser tests

## Test Coverage

- **Unit Tests**: 6 test cases covering all Flask routes
- **Selenium Tests**: 4 test cases for UI functionality
- **Code Quality**: flake8 linting with max line length 120

## Quick Start Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python app.py

# Run unit tests
python -m pytest test_unit.py -v

# Run Selenium tests
python test_selenium.py

# Build Docker image
docker build -t user-management-app .

# Run in container
docker run -p 5000:5000 user-management-app
```

## Assignment Requirements Fulfilled

✅ Web application with database (Flask + SQLite)
✅ GitHub repository integration
✅ Jenkins pipeline with Git integration
✅ Automated Selenium test cases (4 cases)
✅ Docker containerization
✅ Complete CI/CD pipeline stages
✅ GitHub webhook integration capability
✅ Clean, minimal implementation

## Application Features

- Add users with name and email
- View all users in a table
- Delete users with confirmation
- Form validation
- Health check endpoint for monitoring
- Responsive web interface

This is a bare-minimum implementation focused on demonstrating core DevOps concepts without unnecessary complexity.
