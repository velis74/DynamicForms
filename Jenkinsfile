#@IgnoreInspection BashAddShebang
pipeline {
  agent any
  stages {
    stage('build steps') {
      steps {
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
      }
    }
  }
}

def transformIntoStep(env) {
  // We need to wrap what we return in a Groovy closure, or else it's invoked
  // when this method is called, not when we pass it to parallel.
  // To do this, you need to wrap the code below in { }, and either return
  // that explicitly, or use { -> } syntax.
  return {
    stage(env) {
      steps {
      echo "testing ${env}"
      sh """
      #!/bin/bash
      export PATH="/home/jure/.pyenv/bin:$PATH"
      eval "\$(pyenv init -)"
      eval "\$(pyenv virtualenv-init -)"

      pyenv local 3.7.3
      ls -l
      export REMOTE_SELENIUM=\$(REMOTE_SELENIUM_FIREFOX)
      tox -e ${env}"""
      }
    }
  }
}
