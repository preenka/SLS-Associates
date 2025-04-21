pipeline {
    agent any

    environment {
        IMAGE_NAME = "sls-associate"
        IMAGE_TAG = "v2"  // You may want to update this dynamically using Git commit hash or timestamp
        FULL_IMAGE_NAME = "${IMAGE_NAME}:${IMAGE_TAG}"
        CONTAINER_NAME = "sls-container"
    }

    stages {
        stage('Clone Repository') {
            steps {
                // Clone the repository
                git branch: 'main', url: 'https://github.com/preenka/SLS-Associates.git'
            }
        }

        stage('Cleanup Old Container') {
            steps {
                script {
                    // Remove any existing container with the same name
                    sh "docker rm -f ${CONTAINER_NAME} || true"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image
                    sh "docker build -t ${FULL_IMAGE_NAME} ."
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    // Run the container on port 5001
                    sh "docker run -d -p 5001:5000 --name ${CONTAINER_NAME} ${FULL_IMAGE_NAME}"
                }
            }
        }
    }

    post {
        failure {
            // In case of failure, print this message
            echo "Build failed. Check logs above."
        }
        success {
            // If the pipeline succeeds, print this message
            echo "Container '${CONTAINER_NAME}' running at port 5001!"
        }
    }
}
