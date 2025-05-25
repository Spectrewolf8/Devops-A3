pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'user-management-app'
        DOCKER_TAG = "${BUILD_NUMBER}"
        APP_PORT = '5000'
    }
    
    stages {
        stage('Code Linting') {
            steps {
                echo 'Running code linting...'
                bat 'pip install flake8'
                bat 'flake8 app.py test_unit.py test_selenium.py --max-line-length=120 --ignore=E501'
                echo 'Code linting completed'
            }
        }
        
        stage('Code Build') {
            steps {
                echo 'Installing dependencies...'
                bat 'pip install -r requirements.txt'
                echo 'Dependencies installed'
            }
        }
        
        stage('Unit Testing') {
            steps {
                echo 'Running unit tests...'
                bat 'python -m pytest test_unit.py -v'
                echo 'Unit tests completed'
            }
        }
        
        stage('Containerized Deployment') {
            steps {
                echo 'Building and deploying container...'
                bat "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                bat "docker stop user-management-app || echo No container to stop"
                bat "docker rm user-management-app || echo No container to remove"
                bat "docker run -d --name user-management-app -p ${APP_PORT}:5000 ${DOCKER_IMAGE}:${DOCKER_TAG}"
                echo 'Container deployed'
            }
        }
        
        stage('Selenium Testing') {
            steps {
                echo 'Running Selenium tests...'
                sleep 10
                bat "set APP_URL=http://localhost:${APP_PORT} && python test_selenium.py"
                echo 'Selenium tests completed'
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up...'
            bat 'docker stop user-management-app || echo No cleanup needed'
            bat 'docker rm user-management-app || echo No cleanup needed'
        }
    }
}
