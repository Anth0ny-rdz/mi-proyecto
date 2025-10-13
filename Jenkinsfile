pipeline {
    agent any   // Jenkins puede usar cualquier agente disponible

    stages {
        stage('Build') {
            steps {
                echo '🏗️ Etapa de construcción iniciada...'
                sh 'echo Compilando proyecto...'   // Reemplázalo por tu comando real
            }
        }

        stage('Test') {
            steps {
                echo '🧪 Ejecutando pruebas...'
                sh 'echo Corriendo tests simulados...' // Reemplázalo por tus tests
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
