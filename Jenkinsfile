
node {
    stage("first") {
        echo "hello pipeline"
        echo "hello..."
        GIT_BRANCH = sh(returnStdout: true, script: 'git rev-parse --abbrev-ref HEAD').trim()
        echo ${GIT_BRANCH}
    }   
    stage('Test') {
        echo 'Testing....'
    }
    stage('Deploy') {
        echo 'Deploying....'
    }
}
