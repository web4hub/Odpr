[![pipeline status](https://gitlab.electrocnic.com/dood/app/badges/master/pipeline.svg)](https://gitlab.electrocnic.com/dood/app/commits/master)
[![coverage report](https://gitlab.electrocnic.com/dood/app/badges/master/coverage.svg)](https://gitlab.electrocnic.com/dood/app/commits/master)
[![version](https://gitlab.electrocnic.com/dood/app/-/jobs/artifacts/master/raw/latest_release_tag.svg?job=create_badges)](https://gitlab.electrocnic.com/dood/app/commits/master)


# Vue-Django CI/CD template using GitLab, Cypress and Django Unit Tests, and Docker

> This is a Test App to test frontend and backend unit- and integration-tests automated on a CI/CD system.

## Build Setup

To come...

## Template Source

The template is forked from: https://github.com/NdagiStanley/vue-django.git

## More

For a detailed explanation on how things work, check out the [guide](http://vuejs-templates.github.io/webpack/) and [docs for vue-loader](http://vuejs.github.io/vue-loader).


## Gitlab CI/CD


1. Some mandatory variables need to be set in the gitlab-variables settings (Settings->CI/CD->Variables).
Those are listed in the gitlab-ci.yml.
2. Also, the ssh-key file must be set in the variables settings in order to enable auto-deploy. Also add the public key correspondent
to your authorized keys on the deploy server. You need a user on the server for gitlab.
`https://medium.com/@hfally/a-gitlab-ci-config-to-deploy-to-your-server-via-ssh-43bf3cf93775`

3. Your gitlab user must be in the docker group in order to be able to execute docker commands. `sudo gpasswd -a gitlab docker`
4. docker and docker-compose need to be installed on your server.
