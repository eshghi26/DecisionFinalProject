def COLOR_MAP = [
    'SUCCESS': 'good', 
    'FAILURE': 'danger',
]
pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = 'dockerhubcred'
        DOCKERHUB_REPO = 'eshghi26/decisionfinal'
        # DOCKER_SERVER = '192.168.56.17'
        # DOCKER_USER = 'vagrant'
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'git@github.com:eshghi26/DecisionFinalProject.git',
                branch: 'main',
                credentialsId: 'mygitubpk'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    # docker.build("${env.DOCKERHUB_REPO}:${env.BUILD_NUMBER}")
                    dockerImage = docker.build( DOCKERHUB_REPO + ":$BUILD_NUMBER", "./")
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', DOCKERHUB_CREDENTIALS) {
                        # docker.image("${env.DOCKERHUB_REPO}:${env.BUILD_NUMBER}").push()
                        dockerImage.push("V$BUILD_NUMBER")
                        dockerImage.push('latest')
                    }
                }
            }
        }

        stage('Delete image from Jenkins' {
            steps {
                sh "docker rmi $DOCKERHUB_REPO:$BUILD_NUMBER"
            }
        }

        stage('Deploy to Kubernetes') {
            agent {label KOPS}
            steps {
                sh "helm upgrade --install --force decision-stack helm/decisioncharts"
            }
        } 
    }

    post {
        always {
            echo 'Slack Notifications.'
            slackSend channel: '#java-project',
                color: COLOR_MAP[currentBuild.currentResult],
                message: "*${currentBuild.currentResult}:* Job ${env.JOB_NAME} build ${env.BUILD_NUMBER} \n More info at: ${env.BUILD_URL}"
        }
    }
}
