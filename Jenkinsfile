pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/RomiSetty/DevSecOps-Project.git'
        DOCKERHUB_USERNAME = 'romisetty'  // Replace with your Docker Hub username
        DOCKERHUB_REPO = 'project/flask-app' // Replace with your repo name
    }

    stages {
        stage('Clean Up Old Containers') {
            steps {
                script {
                    // Check if any container is using port 5000 and stop it
                    sh '''
                    CONTAINER_ID=$(docker ps -q --filter "expose=5000")
                    if [ ! -z "$CONTAINER_ID" ]; then
                        echo "Stopping container using port 5000: $CONTAINER_ID"
                        docker stop $CONTAINER_ID
                        docker rm $CONTAINER_ID
                    fi
                    docker system prune -f # Remove unused images, containers, and volumes
                    '''
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
                sh '''
                docker run --rm -e PYTHONPATH=/app flask-app pytest
                '''
            }
        }

        stage('Push to Docker Hub') {
            when {
                branch 'main' // Push only when merging to main
            }
            steps {
                script {
                    sh """
                    echo 'Logging into Docker Hub...'
                    echo '${DOCKERHUB_PASSWORD}' | docker login -u '${DOCKERHUB_USERNAME}' --password-stdin
                    docker tag flask-app ${DOCKERHUB_REPO}:latest
                    docker push ${DOCKERHUB_REPO}:latest
                    """
                }
            }
        }

        stage('Deploy') {
            when {
                branch 'main' // Deploy only on 'main' branch
            }
            steps {
                echo "Deploying application from branch: ${env.BRANCH_NAME}"
                sh 'docker run -d -p 5000:5000 --network=host flask-app'
            }
        }
    }
}
