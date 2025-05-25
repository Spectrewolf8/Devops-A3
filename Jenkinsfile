pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'user-management-app'
        DOCKER_TAG = "${BUILD_NUMBER}"
        APP_PORT = '5000'
        PYTHON_IMAGE = 'python:3.11-slim'
    }
    
    stages {
        stage('Code Linting') {
            steps {
                echo 'Running code linting with Python container...'
                script {
                    try {
                        bat """
                            docker run --rm -v "%cd%":/workspace -w /workspace ${PYTHON_IMAGE} sh -c "pip install flake8 && flake8 app.py test_unit.py test_selenium.py --max-line-length=120 --ignore=E501"
                        """
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
                echo 'Installing dependencies and validating build...'
                bat """
                    docker run --rm -v "%cd%":/workspace -w /workspace ${PYTHON_IMAGE} sh -c "pip install -r requirements.txt && python -c \\"import app; print('Build validation successful')\\""
                """
                echo '✓ Dependencies installed and build validated'
            }
        }
        
        stage('Unit Testing') {
            steps {
                echo 'Running unit tests...'
                bat """
                    docker run --rm -v "%cd%":/workspace -w /workspace ${PYTHON_IMAGE} sh -c "pip install -r requirements.txt && python -m pytest test_unit.py -v"
                """
                echo '✓ Unit tests completed'
            }
        }
        
        stage('Containerized Deployment') {
            steps {
                echo 'Building and deploying application container...'
                script {
                    try {
                        // Build Docker image
                        bat "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                        bat "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest"
                        echo "✓ Docker image built: ${DOCKER_IMAGE}:${DOCKER_TAG}"
                        
                        // Stop and remove existing container (Windows syntax)
                        bat """
                            docker stop user-management-app >nul 2>&1 || echo Container not running
                            docker rm user-management-app >nul 2>&1 || echo No container to remove
                        """
                        
                        // Run new container
                        bat "docker run -d --name user-management-app -p ${APP_PORT}:5000 ${DOCKER_IMAGE}:${DOCKER_TAG}"
                        echo "✓ Container deployed on port ${APP_PORT}"
                        
                        // Wait for container to be ready
                        echo 'Waiting for application to start...'
                        sleep 15
                        
                        // Health check
                        bat "docker ps | findstr user-management-app"
                        echo "✓ Container is running successfully"
                        
                    } catch (Exception e) {
                        echo "❌ Deployment failed: ${e.getMessage()}"
                        currentBuild.result = 'FAILURE'
                        error("Container deployment failed")
                    }
                }
            }
        }
        
        stage('Selenium Testing') {
            steps {
                echo 'Running Selenium tests against deployed application...'
                script {
                    try {
                        // Run Selenium tests in container
                        bat """
                            docker run --rm -v "%cd%":/workspace -w /workspace --add-host host.docker.internal:host-gateway ${PYTHON_IMAGE} sh -c "pip install -r requirements.txt && APP_URL=http://host.docker.internal:${APP_PORT} python test_selenium.py"
                        """
                        echo '✓ Selenium tests completed successfully'
                        
                    } catch (Exception e) {
                        echo "❌ Selenium tests failed: ${e.getMessage()}"
                        
                        // Get application logs for debugging
                        try {
                            bat 'docker logs user-management-app'
                        } catch (Exception logError) {
                            echo "Could not get container logs: ${logError.getMessage()}"
                        }
                        
                        // Mark as unstable but continue
                        currentBuild.result = 'UNSTABLE'
                    }
                }
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline execution completed. Cleaning up...'
            script {
                // Stop and remove the application container (Windows syntax)
                try {
                    bat """
                        docker stop user-management-app >nul 2>&1 || echo Container not running
                        docker rm user-management-app >nul 2>&1 || echo No container to remove
                    """
                } catch (Exception e) {
                    echo "Cleanup warning: ${e.getMessage()}"
                }
            }
        }
        
        success {
            echo '🎉 Pipeline completed successfully!'
            echo "✅ All stages passed for build ${BUILD_NUMBER}"
            echo "🌐 Application deployed at: http://localhost:${APP_PORT}"
        }
        
        failure {
            echo '❌ Pipeline failed!'
            echo "🚨 Build ${BUILD_NUMBER} failed. Check logs for details."
        }
        
        unstable {
            echo '⚠ Pipeline completed with warnings'
            echo "🔍 Build ${BUILD_NUMBER} has test failures but deployment succeeded"
        }
    }
}
