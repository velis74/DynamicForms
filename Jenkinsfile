pipeline {
  agent any
  stages {
    stage('build steps') {
      steps {
        echo "building steps"
        script {
          def workspace = "${env.WORKSPACE}"
          def envs = sh(script: '''
            #!/bin/bash
            export PATH="/home/jure/.pyenv/bin:$PATH"
            eval "$(pyenv init -)"
            eval "$(pyenv virtualenv-init -)"

            pyenv local 3.7.3
            tox -l
          ''', returnStdout: true).trim().split('\n')

          def psteps = [:]
          stage('tests') {
            envs.each { env ->
              echo env
              psteps[env] = transformIntoStep('3.7.3', 'FIREFOX', env, "${workspace}")
            }

            psteps['chrome'] = transformIntoStep('3.7.3', 'CHROME', 'py-django22-drf39', "${workspace}")
            psteps['edge'] = transformIntoStep('3.7.3', 'EDGE', 'py-django22-drf39', "${workspace}")
            psteps['ie'] = transformIntoStep('3.7.3', 'IE', 'py-django22-drf39', "${workspace}")
            psteps['safari'] = transformIntoStep('3.7.3', 'SAFARI', 'py-django22-drf39', "${workspace}")
            psteps['python34'] = transformIntoStep('3.4.9', 'FIREFOX', 'py34-django1tip-drf39-typing', "${workspace}")

            parallel psteps
          }
        }
        echo 'done building steps'
      }
    }
  }
}

def transformIntoStep(pyver, browser, env, workspace) {
  // We need to wrap what we return in a Groovy closure, or else it's invoked
  // when this method is called, not when we pass it to parallel.
  // To do this, you need to wrap the code below in { }, and either return
  // that explicitly, or use { -> } syntax.
  return {
    agent {
    node {
      echo "testing ${env}"
      deleteDir()
      sh """
      #!/bin/bash
      export PATH="/home/jure/.pyenv/bin:$PATH"
      eval "\$(pyenv init -)"
      eval "\$(pyenv virtualenv-init -)"

      rsync -rtpl ${workspace}/. .
      if [ -d "${workspace}/.tox/${env}" ]; then
        rsync -rtpl ${workspace}/.tox/${env} .tox
      fi

      pyenv local ${pyver}
      export REMOTE_SELENIUM=\$REMOTE_SELENIUM_${browser}
      tox -e ${env}
      rsync -rtpl .tox/${env} ${workspace}/.tox
      """
      deleteDir()
    }
    }
  }
}
