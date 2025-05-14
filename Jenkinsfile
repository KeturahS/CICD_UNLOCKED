pipeline {
    agent any

    environment {
        DJANGO_SETTINGS_MODULE = 'CICD__UNLOCKED.settings'
        PYTHONPATH = 'CICD__UNLOCKED'
    }

    stages {
        stage('Create Virtual Env') {
            steps {
                sh 'python3 -m venv venv'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install django pytest pytest-django
                '''
            }
        }

        stage('Build') {
            steps {
                echo 'Checking for syntax errors...'
                sh 'python3 -m py_compile CICD__UNLOCKED/App_SetUp/*.py'
            }
        }

        stage('Test') {
            steps {
                echo 'Running pytest tests...'
                sh '''
                    . venv/bin/activate
                    pytest --ds=CICD__UNLOCKED.settings --junit-xml=test-reports/results.xml
                '''
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                }
            }
        }
    }
}
