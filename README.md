# User Management System - DevOps Assignment

A simple Flask web application demonstrating CI/CD pipeline with Jenkins, Docker, and automated testing.

## 🎯 Assignment Requirements

This project fulfills the DevOps assignment requirements:

- ✅ Simple Web application with Database Server (Flask + SQLite)
- ✅ GitHub repository integration
- ✅ Jenkins pipeline with Git integration
- ✅ Automated Selenium test cases (4 test cases)
- ✅ Docker containerization for deployment
- ✅ Complete CI/CD pipeline with stages:
  - Code Linting stage (flake8)
  - Code Build stage (Docker build)
  - Unit Testing stage (pytest)
  - Containerized Deployment stage (Docker)
  - Selenium Testing stage

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite
- **Testing**: pytest (unit tests), Selenium (integration tests)
- **Containerization**: Docker
- **CI/CD**: Jenkins
- **Code Quality**: flake8 linting

## 📋 Prerequisites

- Python 3.9+
- Docker Desktop
- Jenkins (for CI/CD pipeline)
- Git

## 🚀 Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python app.py
```

Application will be available at: http://localhost:5000

### 3. Run Tests

**Unit Tests:**

```bash
python -m pytest test_unit.py -v
```

**Selenium Tests:**

```bash
python test_selenium.py
```

**Code Linting:**

```bash
flake8 app.py test_unit.py test_selenium.py --max-line-length=120
```

## 🐳 Docker Setup

### Build and Run Container

```bash
docker build -t user-management-app .
docker run -p 5000:5000 user-management-app
```

### Using Docker Compose

```bash
docker-compose up --build
```

## 🚀 Jenkins Pipeline

### Required Jenkins Plugins

- Git Plugin
- Pipeline Plugin
- Docker Pipeline Plugin
- GitHub Integration Plugin

### Pipeline Stages

1. **Checkout** - Fetch code from GitHub
2. **Code Linting** - flake8 code quality checks
3. **Unit Testing** - pytest unit tests
4. **Build Docker Image** - Create containerized application
5. **Containerized Deployment** - Deploy application in Docker
6. **Selenium Testing** - Automated browser tests

### Jenkins Setup Steps

1. Create new Pipeline job in Jenkins
2. Configure SCM to point to your GitHub repository
3. Set Script Path to `Jenkinsfile`
4. Ensure Jenkins agent has Python, Docker, and Chrome installed

## 📁 Project Structure

```
├── app.py                 # Flask application
├── templates/
│   ├── index.html        # Home page template
│   └── add_user.html     # Add user form template
├── test_unit.py          # Unit tests (pytest)
├── test_selenium.py      # Selenium tests (4 test cases)
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose setup
├── Jenkinsfile          # Jenkins pipeline script
└── README.md            # This documentation
```

## 🧪 Test Cases

### Unit Tests (test_unit.py)

- Home page loading
- Add user functionality
- Form validation
- User deletion
- Health check endpoint

### Selenium Tests (test_selenium.py)

1. **Home Page Load Test** - Verifies main page loads correctly
2. **Add User Functionality** - Tests complete user creation workflow
3. **Form Validation** - Tests client-side validation
4. **Navigation** - Tests page navigation between forms

## 🔧 GitHub Integration

1. **Push to GitHub:**

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Configure Jenkins Webhook (Optional):**
   - GitHub repository settings → Webhooks
   - Add webhook: `http://your-jenkins-url/github-webhook/`

## 🐛 Troubleshooting

### Common Issues

**Selenium Tests Fail:**

- Ensure Chrome browser is installed
- Check application is running on correct port
- Verify network connectivity

**Docker Build Fails:**

- Check Docker daemon is running
- Verify sufficient disk space

**Jenkins Pipeline Fails:**

- Ensure Jenkins agent has Python, Docker, Chrome installed
- Check workspace permissions

### Debug Commands

**Check Application Health:**

```bash
curl http://localhost:5000/health
```

**View Docker Logs:**

```bash
docker logs user-management-app
```

## 📝 Assignment Submission Checklist

- ✅ Flask web application with SQLite database
- ✅ GitHub repository with complete code
- ✅ Jenkinsfile with all required stages
- ✅ Unit tests using pytest
- ✅ Selenium tests (minimum 2 test cases - we have 4)
- ✅ Docker containerization
- ✅ CI/CD pipeline documentation
- ✅ README with setup instructions

## 🎓 Educational Purpose

This project is created for a DevOps course assignment demonstrating:

- Continuous Integration/Continuous Deployment (CI/CD)
- Automated testing strategies
- Containerization with Docker
- Infrastructure as Code with Jenkins pipelines
- Version control integration with Git/GitHub
