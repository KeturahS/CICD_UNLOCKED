pipeline {
    agent any

    environment {
        DJANGO_SETTINGS_MODULE = 'CICD__UNLOCKED.settings'
        PYTHONPATH = 'CICD__UNLOCKED'
    }

    stages {
        stage('Install Dependencies') {
            steps {
                sh '''
                    pip3 install --upgrade pip
                    pip3 install django pytest pytest-django pandas matplotlib psutil arabic-reshaper python-bidi
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
                sh '~/.local/bin/pytest --ds=CICD__UNLOCKED.settings --junit-xml=test-reports/results.xml'
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                }
            }
        }

    }
}
