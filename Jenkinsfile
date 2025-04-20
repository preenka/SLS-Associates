pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/preenka/SLS-Associates.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build('sls-associates:latest')
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    dockerImage.run('-p 8000:8000')
                }
            }
        }
    }
}
