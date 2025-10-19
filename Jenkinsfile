pipeline {
    agent any

    environment {
        PYTHON_HOME = 'C:\\Users\\Didier\\AppData\\Local\\Programs\\Python\\Python312'
        PATH = "${env.PYTHON_HOME};${env.PYTHON_HOME}\\Scripts;${env.PATH}"
    }

    stages {
        stage('Check Python') {
            steps {
                bat 'python --version'
                bat 'pip --version'
            }
        }

        stage('Build') {
            steps {
                echo " Creando entorno virtual e instalando dependencias..."
                bat '''
                python -m venv venv
                call venv\\Scripts\\activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Test with Coverage') {
            steps {
                echo " Ejecutando pruebas con cobertura..."
                bat '''
                call venv\\Scripts\\activate
                pytest --cov=app --cov-report=xml --disable-warnings -q
                '''
            }
            post {
                always {
                    junit 'tests/**/*.xml'
                    echo " Tests ejecutados"
                }
            }
        }

        stage('Code Quality') {
            steps {
                echo " Analizando código con flake8..."
                bat '''
                call venv\\Scripts\\activate
                flake8 app --statistics --count --show-source
                '''
            }
        }

        stage('Deploy Simulation') {
            steps {
                echo " Simulando despliegue (build Flask app)..."
                bat '''
                call venv\\Scripts\\activate
                python app/api.py
                '''
            }
        }
    }

    post {
        success {
            echo " Pipeline completado con éxito."
        }
        failure {
            echo " Falló alguna etapa. Revisar logs."
        }
        always {
            echo " Fin del pipeline."
        }
    }
}
