pipeline {
    agent any

    environment {
        IMAGE_NAME = 'jenkins/jenkins:jdk17'
        CONTAINER_NAME = 'my-jenkins-container'
        PORT = '9090'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/preenka/SLS-Associates.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build Docker image
                    dockerImage = docker.build("${IMAGE_NAME}:latest")
                }
            }
        }

        stage('Stop Existing Container') {
            steps {
                script {
                    // Stop and remove the old container if it exists
                    sh """
                        docker stop ${CONTAINER_NAME} || true
                        docker rm ${CONTAINER_NAME} || true
                    """
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    // Run the new Docker container with the correct port binding
                    sh """
                        docker run -d -p ${PORT}:${PORT} --name ${CONTAINER_NAME} ${IMAGE_NAME}:latest
                    """
                }
            }
        }
    }
}
