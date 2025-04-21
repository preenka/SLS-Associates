pipeline {
    agent any

    environment {
        IMAGE_NAME = "sls-associate"
        IMAGE_TAG = "v2"  // Adjusted to reflect the image version
        FULL_IMAGE_NAME = "${IMAGE_NAME}:${IMAGE_TAG}"
        CONTAINER_NAME = "sls-container"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/preenka/SLS-Associates.git'
            }
        }

        stage('Cleanup Old Container') {
            steps {
                script {
                    bat "docker rm -f ${CONTAINER_NAME} || echo 'No container to remove'"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    bat "docker build -t ${FULL_IMAGE_NAME} ."
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    bat "docker run -d -p 5001:5000 --name ${CONTAINER_NAME} ${FULL_IMAGE_NAME}"
                }
            }
        }
    }

    post {
        failure {
            echo "Build failed. Check logs above."
        }
        success {
            echo "Container '${CONTAINER_NAME}' is running at port 5001!"
        }
    }
}
