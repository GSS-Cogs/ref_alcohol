pipeline {
    agent {
        label 'master'
    }
    stages {
        stage('Test') {
            agent {
                docker {
                    image 'cloudfluff/csvlint'
                    reuseNode true
                }
            }
            steps {
                script {
                    sh "csvlint -s codelists-metadata.json"
                }
            }
        }
        stage('Upload draftset') {
            steps {
                script {
                    jobDraft.replace()
                    def codelists = readJSON(file: 'codelists-metadata.json')
                    for (def table : codelists['tables']) {
                        String codelistFilename = table['url']
                        String label = table['rdfs:label']
                        uploadCodelist(codelistFilename, label)
                    }
                    uploadComponents("components.csv")
                }
            }
        }
        stage('Publish') {
            steps {
                script {
                    jobDraft.publish()
                }
            }
        }
    }
    post {
        success {
            build job: '../GDP-tests', wait: false
        }
    }
}
