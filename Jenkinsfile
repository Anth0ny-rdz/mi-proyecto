pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo "Instalando dependencias..."
                sh 'python -m venv venv'
                sh './venv/bin/pip install -r requirements.txt'
            }
        }

        stage('Test and Lint') {
            steps {
                echo "Ejecutando pruebas y análisis de calidad..."
                sh './venv/bin/pytest --maxfail=1 --disable-warnings -q'
                sh './venv/bin/flake8 app --count --select=E9,F63,F7,F82 --show-source --statistics'
            }
            post {
                always {
                    junit '**/test-results/*.xml'
                }
                success {
                    echo "✅ Todas las pruebas pasaron correctamente."
                }
                failure {
                    echo "❌ Error en pruebas o calidad de código."
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline finalizado."
        }
    }
}