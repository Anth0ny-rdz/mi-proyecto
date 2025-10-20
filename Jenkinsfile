pipeline {
    agent any

    environment {
        // Ruta al Python que Jenkins usará (ajústala si usas otra versión)
        PYTHON_HOME = 'C:\\Users\\Didier\\AppData\\Local\\Programs\\Python\\Python312'
        PATH = "${env.PYTHON_HOME};${env.PYTHON_HOME}\\Scripts;${env.PATH}"
    }

    stages {

        stage('Check Python') {
            steps {
                echo "🔍 Verificando instalación de Python..."
                bat 'python --version'
                bat 'pip --version'
            }
        }

        stage('Build') {
            steps {
                echo "🏗️ Creando entorno virtual e instalando dependencias..."
                bat '''
                python -m venv venv
                call venv\\Scripts\\activate
                python -m pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests and Coverage') {
            steps {
                echo "🧪 Ejecutando pruebas y cobertura..."
                bat '''
                call venv\\Scripts\\activate
                pytest --maxfail=1 --disable-warnings --cov=app --cov-report=xml --html=pytest_report.html --self-contained-html
                '''
            }
        }

        stage('Code Quality') {
            steps {
                echo "🔎 Analizando calidad del código..."
                bat '''
                call venv\\Scripts\\activate
                flake8 app --format=html --htmldir=flake-report || echo "⚠️ Flake8 encontró advertencias."
                python -m pylint app > pylint-report.txt || echo "⚠️ Pylint encontró advertencias."
                '''
            }
        }

        stage('Security Scan') {
            steps {
                echo "🛡️ Escaneando seguridad..."
                bat '''
                call venv\\Scripts\\activate
                bandit -r app -f txt -o bandit-report.txt || echo "⚠️ Bandit falló o encontró vulnerabilidades, pero no se detiene el pipeline."
                '''
            }
        }

        stage('Archive Reports') {
            steps {
                echo "📦 Guardando reportes..."
                archiveArtifacts artifacts: '**/*.html, **/*.xml, **/*.txt, logs/*.log', fingerprint: true
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline completado exitosamente."
        }
        failure {
            echo "❌ Falló alguna etapa. Revisar logs y reportes generados."
        }
        always {
            echo "🏁 Fin del pipeline."
        }
    }
}
