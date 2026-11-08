pipeline {
    agent any

    options {
        timestamps()
    }

    environment {
        PY = 'C:\\Program Files\\Python313\\python.exe'
    }

    stages {

        stage('Check Environment') {
            steps {
                bat '"%PY%" --version'
                bat 'git --version'
                powershell '''
                try {
                    Invoke-WebRequest -Uri "http://127.0.0.1:8000" -UseBasicParsing -TimeoutSec 5 | Out-Null
                    Write-Host "Pretix is reachable."
                } catch {
                    Write-Error "Pretix is not running at http://127.0.0.1:8000"
                    exit 1
                }
                '''
            }
        }

        stage('Setup Python Environment') {
            steps {
                bat 'if not exist .venv\\Scripts\\python.exe "%PY%" -m venv .venv'
                bat '.venv\\Scripts\\python.exe -m pip install --upgrade pip'
                bat '.venv\\Scripts\\python.exe -m pip install -r requirements.txt'
            }
        }

        stage('Run Selenium Tests') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'pretix-admin-credentials',
                    usernameVariable: 'ADMIN_EMAIL',
                    passwordVariable: 'ADMIN_PASSWORD')]) {
                    bat '.venv\\Scripts\\python.exe -m pytest tests/ -v --html=report.html --self-contained-html'
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'report.html', allowEmptyArchive: true
        }
    }
}