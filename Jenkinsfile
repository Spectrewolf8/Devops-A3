pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
        }
    }
    
    environment {
        DOCKER_IMAGE = 'user-management-app'
        DOCKER_TAG = "${BUILD_NUMBER}"
        APP_PORT = '5000'
    }
    
    stages {
        stage('Setup Environment') {
            steps {
                echo 'Setting up environment...'
                sh '''
                    apt-get update
                    apt-get install -y docker.io curl
                    python --version
                    pip --version
                '''
            }
        }
        
        stage('Code Linting') {
            steps {
                echo 'Running code linting...'
                script {
                    try {
                        sh 'pip install flake8'
                        sh 'flake8 app.py test_unit.py test_selenium.py --max-line-length=120 --ignore=E501'
                        echo '✓ Code linting passed'
                    } catch (Exception e) {
                        echo "⚠ Linting warnings: ${e.getMessage()}"
                        // Continue pipeline
                    }
                }
            }
        }
        
        stage('Code Build') {
            steps {
                echo 'Installing dependencies...'
                sh 'pip install -r requirements.txt'
                echo 'Dependencies installed'
            }
        }
        
        stage('Unit Testing') {
            steps {
                echo 'Running unit tests...'
                sh 'python -m pytest test_unit.py -v'
                echo 'Unit tests completed'
            }
        }
        
        stage('Containerized Deployment') {
            steps {
                echo 'Building and deploying container...'
                sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                sh "docker stop user-management-app || echo 'No container to stop'"
                sh "docker rm user-management-app || echo 'No container to remove'"
                sh "docker run -d --name user-management-app -p ${APP_PORT}:5000 ${DOCKER_IMAGE}:${DOCKER_TAG}"
                echo 'Container deployed'
            }
        }
        
        stage('Selenium Testing') {
            steps {
                echo 'Running Selenium tests...'
                sh 'sleep 10'
                sh "APP_URL=http://localhost:${APP_PORT} python test_selenium.py"
                echo 'Selenium tests completed'
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up...'
            script {
                try {
                    sh 'docker stop user-management-app || echo "No container to stop"'
                } catch (Exception e) {
                    echo "Container stop: ${e.getMessage()}"
                }
                try {
                    sh 'docker rm user-management-app || echo "No container to remove"'
                } catch (Exception e) {
                    echo "Container remove: ${e.getMessage()}"
                }
            }
        }
    }
}
