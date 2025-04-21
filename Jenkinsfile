pipeline {
    agent any

    environment {
        IMAGE_NAME = "SLS-Associate"
        IMAGE_TAG = "v1"
        FULL_IMAGE_NAME = "${IMAGE_NAME}:${IMAGE_TAG}"
        CONTAINER_NAME = "SLS-Associates"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/preenka/SLS-Associates.git'
            }
        }

        stage('Cleanup Old Container (Optional)') {
            steps {
                script {
                    sh "docker rm -f $CONTAINER_NAME || true"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker version' // Verify Docker works
                    sh "docker build -t $FULL_IMAGE_NAME ."
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    sh 'docker run -d -p 5001:5000 --name SLS_container SLS_app:v1'
                }
            }
        }
    }
}