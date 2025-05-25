pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'user-management-app'
        DOCKER_TAG = "${BUILD_NUMBER}"
        APP_PORT = '5000'
        GITHUB_REPO = 'your-github-username/user-management-app'
    }
    
    stages {
        stage('Code Linting') {
            steps {
                echo 'Running code linting with flake8...'
                script {
                    try {
                        // Install dependencies for linting
                        bat 'pip install flake8'
                        
                        // Run flake8 linting
                        bat 'flake8 app.py test_unit.py test_selenium.py --max-line-length=120 --ignore=E501,W503'
                        
                        echo '✓ Code linting passed'
                    } catch (Exception e) {
                        echo "⚠ Linting warnings found: ${e.getMessage()}"
                        // Continue pipeline even with linting warnings
                    }
                }
            }
        }
        
        stage('Code Build') {
            steps {
                echo 'Installing Python dependencies...'
                bat 'pip install -r requirements.txt'
                echo '✓ Dependencies installed successfully'
            }
        }
        
        stage('Unit Testing') {
            steps {
                echo 'Running unit tests...'
                script {
                    try {
                        bat 'python -m pytest test_unit.py -v --tb=short'
                        echo '✓ Unit tests passed'
                    } catch (Exception e) {
                        echo "❌ Unit tests failed: ${e.getMessage()}"
                        currentBuild.result = 'FAILURE'
                        error("Unit tests failed")
                    }
                }
            }
            post {
                always {
                    // Archive test results if they exist
                    script {
                        if (fileExists('test-results.xml')) {
                            archiveArtifacts artifacts: 'test-results.xml', fingerprint: true
                        }
                    }
                }
            }
        }
        
        stage('Containerized Deployment') {
            steps {
                echo 'Building Docker image and deploying application...'
                script {
                    try {
                        // Build Docker image
                        bat "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                        bat "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest"
                        echo "✓ Docker image built: ${DOCKER_IMAGE}:${DOCKER_TAG}"
                        
                        // Stop and remove existing container if it exists
                        bat '''
                            docker stop user-management-app || echo "No container to stop"
                            docker rm user-management-app || echo "No container to remove"
                        '''
                        
                        // Run new container
                        bat """
                            docker run -d ^
                                --name user-management-app ^
                                -p ${APP_PORT}:5000 ^
                                --health-cmd="curl -f http://localhost:5000/health || exit 1" ^
                                --health-interval=30s ^
                                --health-timeout=10s ^
                                --health-retries=3 ^
                                ${DOCKER_IMAGE}:${DOCKER_TAG}
                        """
                        
                        // Wait for application to be healthy
                        echo 'Waiting for application to be healthy...'
                        timeout(time: 2, unit: 'MINUTES') {
                            waitUntil {
                                script {
                                    def result = bat(
                                        script: 'docker inspect --format="{{.State.Health.Status}}" user-management-app',
                                        returnStdout: true
                                    ).trim()
                                    return result == 'healthy'
                                }
                            }
                        }
                        
                        echo "✓ Application deployed and healthy on port ${APP_PORT}"
                        
                    } catch (Exception e) {
                        echo "❌ Deployment failed: ${e.getMessage()}"
                        currentBuild.result = 'FAILURE'
                        error("Deployment failed")
                    }
                }
            }
        }
        
        stage('Selenium Testing') {
            steps {
                echo 'Running Selenium tests against deployed application...'
                script {
                    try {
                        // Set environment variable for Selenium tests
                        bat "set APP_URL=http://localhost:${APP_PORT} && python test_selenium.py"
                        echo '✓ Selenium tests passed'
                        
                    } catch (Exception e) {
                        echo "❌ Selenium tests failed: ${e.getMessage()}"
                        
                        // Get application logs for debugging
                        bat 'docker logs user-management-app'
                        
                        currentBuild.result = 'FAILURE'
                        error("Selenium tests failed")
                    }
                }
            }
            post {
                always {
                    script {
                        // Capture screenshots if they exist
                        if (fileExists('screenshots')) {
                            archiveArtifacts artifacts: 'screenshots/**', fingerprint: true
                        }
                        
                        // Get container logs
                        try {
                            bat 'docker logs user-management-app > app-logs.txt 2>&1'
                            archiveArtifacts artifacts: 'app-logs.txt', fingerprint: true
                        } catch (Exception e) {
                            echo "Could not capture application logs: ${e.getMessage()}"
                        }
                    }
                }
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline execution completed'
            
            script {
                // Clean up containers
                try {
                    bat '''
                        docker stop user-management-app || echo "No container to stop"
                        docker rm user-management-app || echo "No container to remove"
                    '''
                } catch (Exception e) {
                    echo "Cleanup warning: ${e.getMessage()}"
                }
                
                // Clean up old Docker images (keep last 5 builds)
                try {
                    bat """
                        for /f "tokens=3" %%i in ('docker images ${DOCKER_IMAGE} --format "table {{.Tag}}" ^| findstr /R "^[0-9]"') do (
                            if %%i LEQ ${BUILD_NUMBER - 5} (
                                docker rmi ${DOCKER_IMAGE}:%%i || echo "Could not remove image ${DOCKER_IMAGE}:%%i"
                            )
                        )
                    """
                } catch (Exception e) {
                    echo "Image cleanup warning: ${e.getMessage()}"
                }
            }
        }
        
        success {
            echo '🎉 Pipeline completed successfully!'
            script {
                // Send success notification (you can configure email, Slack, etc.)
                echo "✅ Build ${BUILD_NUMBER} completed successfully"
                echo "📦 Docker image: ${DOCKER_IMAGE}:${DOCKER_TAG}"
                echo "🌐 Application available at: http://localhost:${APP_PORT}"
            }
        }
        
        failure {
            echo '❌ Pipeline failed!'
            script {
                echo "🚨 Build ${BUILD_NUMBER} failed"
                echo "📝 Check the logs above for error details"
                echo "🔧 Common issues:"
                echo "  - Check if all dependencies are installed"
                echo "  - Verify Docker is running"
                echo "  - Check application health
