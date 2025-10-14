pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo "Instalando dependencias..."
                bat '''
                python -m venv venv
                call venv\Scripts\activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Test and Lint') {
            steps {
                echo "Ejecutando pruebas y análisis de calidad..."
                bat '''
                call venv\Scripts\activate
                pytest --maxfail=1 --disable-warnings -q
                flake8 app --count --select=E9,F63,F7,F82 --show-source --statistics
                '''
            }
        }
    }

    post {
        always {
            echo "Pipeline finalizado."
        }
    }
}