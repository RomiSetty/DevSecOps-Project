pipeline {
    agent any

    environment {
        DOCKERHUB_USERNAME = 'romisetty'  // Replace with your Docker Hub username
        DOCKERHUB_REPO = 'romisetty/project' // Replace with your repo name
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
            steps {
                echo "Running tests for ${env.BRANCH_NAME}"
                sh "docker run --rm -e PYTHONPATH=/app flask-app pytest"
            }
        }

        stage('Push to Docker Hub') {
            when {
                branch 'main' // Push only when merging to main
            }
            steps {
                script {
                    def currentDate = new Date().format("yyyy-MM-dd-HH:mm")
                    withCredentials([usernamePassword(credentialsId: 'DOCKERHUB_CREDENTIALS', usernameVariable: 'DOCKERHUB_USERNAME', passwordVariable: 'DOCKERHUB_PASSWORD')]) {
                        sh """
                        echo 'Logging into Docker Hub...'
                        docker login -u '${DOCKERHUB_USERNAME}' -p '${DOCKERHUB_PASSWORD}'
                        docker tag flask-app ${DOCKERHUB_REPO}:${currentDate}
                        docker push ${DOCKERHUB_REPO}:${currentDate}
                        """
                    }
                }
            }
        }

        stage('Deploy') {
            when {
                branch 'main' // Deploy only on 'main' branch
            }
            steps {
                echo "Deploying application from branch: ${env.BRANCH_NAME}"
                //manual deploy for now
                // other options : AWS on EC2 OR EKS using terraform.
            }
        }
    }
}
