
node {
    stage("first") {
        echo "hello pipeline"
        echo "hello..."
    
        echo "git commit hash: ${env.GIT_COMMIT}"

        $GIT_BRANCH = sh(returnStdout: true, script: 'git rev-parse --abbrev-ref HEAD').trim()
        echo "branch name: $GIT_BRANCH"
        
    }   
    stage('Test') {
        echo 'Testing....'
    }
    stage('Deploy') {
        echo 'Deploying....'
    }
}
