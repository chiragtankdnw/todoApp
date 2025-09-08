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

        stage('Setup Python Environment - Django') {
            steps {
                bat '''
                python -m venv %VENV_DIR%
                call %VENV_DIR%\\Scripts\\activate
                pip install --upgrade pip
                pip install -r requirements.txt
                python manage.py migrate
                '''
            }
        }

        stage('Frontend Setup - React') {
            steps {
                dir('frontend') {
                    bat '''
                    npm install
                    npm run build
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                bat '''
                call %VENV_DIR%\\Scripts\\activate
                taskkill /F /IM python.exe || echo "No python process"
                start /B python manage.py runserver 0.0.0.0:8000
                '''
            }
        }
    }
}
