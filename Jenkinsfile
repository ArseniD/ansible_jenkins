node("${env.SLAVE}") {

  stage("Build"){
    /*
        Update file src/main/resources/build-info.txt with following details:
        - Build time
        - Build Machine Name
        - Build User Name
        - GIT URL: ${GIT_URL}
        - GIT Commit: ${GIT_COMMIT}
        - GIT Branch: ${GIT_BRANCH}

        Simple command to perform build is as follows:
        $ mvn clean package -DbuildNumber=$BUILD_NUMBER
        sh "echo Build time: 18:00 > src/main/resources/build-info.txt"
        sh "echo Build Machine Name: epbyminw2472 >> src/main/resources/build-info.txt"
        sh "echo Build User Name: student >> src/main/resources/build-info.txt"
    */
    git branch: 'master', url: 'https://github.com/ArseniD/mntlab-exam'
    sh "echo build artefact"
    sh "mvn clean package -DbuildNumber=$BUILD_NUMBER"
  }

  stage("Package"){
    /*
        use tar tool to package built war file into *.tar.gz package
    */
    sh "echo package artefact"
    sh "tar czf mnt-exam-${BUILD_NUMBER}.tar.gz target/mnt-exam.war"
  }

  stage("Roll out Dev VM"){
    /*
        use ansible to create VM (with developed vagrant module)
    */
    sh "ansible-playbook createvm.yml"
  }

  stage("Provision VM"){
    /*
        use ansible to provision VM
        Tomcat and nginx should be installed
    */
    sh "ansible-playbook provisionvm.yml"
  }

  stage("Deploy Artefact"){
    /*
        use ansible to deploy artefact on VM (Tomcat)
        During the deployment you should create file: /var/lib/tomcat/webapps/deploy-info.txt
        Put following details into this file:
        - Deployment time
        - Deploy User
        - Deployment Job
        sh "echo Build time: 18:10 >> src/main/resources/build-info.txt"
        sh "echo Deploy User: $USER >> src/main/resources/build-info.txt"
        sh "echo Deployment Job: Deploy Artefact >> /var/lib/tomcat/webapps/deploy-info.txt"
        sh "echo  >> /var/lib/tomcat/webapps/deploy-info.txt"
    */
    sh "ansible-playbook deploy.yml -e artefact=target/mnt-exam.war"
  }

  stage("Test Artefact is deployed successfully"){
    /*
        use ansible to artefact on VM (Tomcat)
        During the deployment you should create file: /var/lib/tomcat/webapps/deploy-info.txt
        Put following details into this file:
        - Deployment time
        - Deploy User
        - Deployment Job
         sh "echo Build time: 18:10 >> /var/lib/tomcat/webapps/deploy-info.txt"
        sh "echo Deploy User: $USER >> /var/lib/tomcat/webapps/deploy-info.txt"
        sh "echo Deployment Job: Test Artefact is deployed successfully >> /var/lib/tomcat/webapps/deploy-info.txt"
        sh "echo  >> /var/lib/tomcat/webapps/deploy-info.txt"
    */
    sh "ansible-playbook application_tests.yml -e artefact=target/mnt-exam.war"
    sleep 30
  }
}

