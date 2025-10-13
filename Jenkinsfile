pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo '🏗️ Etapa de construcción iniciada...'
                bat '"C:\\Windows\\System32\\cmd.exe" /c echo Compilando proyecto...'
            }
        }

        stage('Test') {
            steps {
                echo '🧪 Ejecutando pruebas...'
                bat '"C:\\Windows\\System32\\cmd.exe" /c echo Corriendo tests simulados...'
            }
        }
    }

    post {
        success {
            echo '✅ Todo salió bien.'
        }
        failure {
            echo '❌ El pipeline falló.'
        }
        always {
            echo "Pipeline completado. Estado final: ${currentBuild.currentResult}"
        }
    }
}

