# cicd-for-lotti
The repository for the CI/CD files for the family of projects:
[Lotti Karotti-calculator](https://github.com/ssichynskyi/lotti-karotti-calculator)
and
[Lotti Karotti-calculator-testing-task](https://github.com/ssichynskyi/testing-task-lotti-karotti-calculator)

# Content
## Linux
folder "linux" contains all necessary for building for this OS:
- folder "local" contains bash files to execute testing and compilation on local linux and windows PC
- main folder contains jenkinsfile for CI on jenkinsfile other resources specific to Jenkins are stored
in "jenkins" folder
- common resources for both solutions stored in folder "common"
## Windows
folder "linux" contains all necessary for building for this OS:
-TBD

# Usage
## Local build
Run:
- "rebuild_docker_images.sh" (run for the first time and every time the dockerfiles are updated)
- "test-build-deploy.sh" (run everytime the new build is required)
For simplification it's also possible to run the single script "test-build-deploy-clean.sh" which sequentially combines the execution of "rebuild_docker_images.sh" and "test-build-deploy.sh"


## Jenkins build
- use jenkinsfile in SCM pipeline plugin for Jenkins
