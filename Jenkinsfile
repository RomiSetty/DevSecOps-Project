pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/RomiSetty/DevSecOps-Project.git'
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    cleanWs() // Clean workspace to remove old files
                    checkout([
                        $class: 'GitSCM',
                        branches: [[name: "*/${env.BRANCH_NAME}"]],
                        userRemoteConfigs: [[url: REPO_URL]]
                    ])
                    echo "Checked out branch: ${env.BRANCH_NAME}"
                }
            }
        }

        stage('Build') {
            steps {
                echo "Building branch: ${env.BRANCH_NAME}"
                sh 'docker build -t flask-app .'
            }
        }

        stage('Test') {
            when {
                not {
                    branch 'main' // Exclude tests from running on 'main'
                }
            }
            steps {
                echo "Running tests for ${env.BRANCH_NAME}"
                sh 'docker run --rm flask-app pytest'
            }
        }

        stage('Deploy') {
            when {
                branch 'main' // Deploy only on 'main' branch
            }
            steps {
                echo "Deploying application from branch: ${env.BRANCH_NAME}"
                sh 'docker run -d -p 5000:5000 flask-app'
            }
        }
    }
}
