pipeline {
    agent any

    environment {
        VENV_DIR = "venv"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/chiragtankdnw/todoApp.git'
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                python3 -m venv $VENV_DIR
                . $VENV_DIR/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '''
                . $VENV_DIR/bin/activate
                python manage.py test
                '''
            }
        }
    }

    post {
        always {
            junit '**/TEST-*.xml' allowEmptyResults: true
        }
    }
}
