pipeline {
  agent any
  stages {
    stage('build steps') {
      steps {
/*
        echo "building steps"
        script {
          def psteps = [:]
          def envs = sh(script: '''
            #!/bin/bash
            export PATH="/home/jure/.pyenv/bin:$PATH"
            eval "$(pyenv init -)"
            eval "$(pyenv virtualenv-init -)"

            pyenv local 3.7.3
            tox -l
          ''', returnStdout: true).trim().split('\n')
          envs.each { env ->
            echo env
            psteps[env] = transformIntoStep(env)
          }
          parallel psteps
        }
        echo 'done building steps'
*/
/*
      sh """
      #!/bin/bash
      export PATH="/home/jure/.pyenv/bin:$PATH"
      eval "\$(pyenv init -)"
      eval "\$(pyenv virtualenv-init -)"

      pyenv local 3.7.3
      export REMOTE_SELENIUM=\$REMOTE_SELENIUM_FIREFOX
      tox -p auto
      """
*/
        parallel(
          'standard': transformIntoStep('3.7.3', 'FIREFOX', 'all'),
          'check': transformIntoStep('3.7.3', 'CHROME', 'check'),
          'doc': transformIntoStep('3.7.3', 'CHROME', 'doc'),
          'chrome': transformIntoStep('3.7.3', 'CHROME', 'py-django22-drf39'),
          'edge': transformIntoStep('3.7.3', 'EDGE', 'py-django22-drf39'),
          'ie': transformIntoStep('3.7.3', 'IE', 'py-django22-drf39'),
          'safari': transformIntoStep('3.7.3', 'SAFARI', 'py-django22-drf39'),
          'python34': transformIntoStep('3.4.9', 'FIREFOX', 'py34-django1tip-drf39-typing')
        }
      }
    }
  }
}

def transformIntoStep(pyver, browser, env) {
  // We need to wrap what we return in a Groovy closure, or else it's invoked
  // when this method is called, not when we pass it to parallel.
  // To do this, you need to wrap the code below in { }, and either return
  // that explicitly, or use { -> } syntax.
  return {
    node {
      echo "testing ${env}"
      sh """
      #!/bin/bash
      export PATH="/home/jure/.pyenv/bin:$PATH"
      eval "\$(pyenv init -)"
      eval "\$(pyenv virtualenv-init -)"

      pyenv local ${pyver}
      pwd
      export REMOTE_SELENIUM=\$REMOTE_SELENIUM_${browser}
      tox -e ${env}"""
    }
  }
}
