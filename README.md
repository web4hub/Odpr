<!-- Badges are (except for pipeline status and coverage report) created in util/run_lighthouse.sh, there they will also be uploaded to the URLs listed below. -->
[![version](https://test.gitlab.electrocnic.com/gitlab-badges/latest_release_tag.svg)](https://gitlab.electrocnic.com/dood/app/commits/master)
[![pipeline status](https://gitlab.electrocnic.com/dood/app/badges/master/pipeline.svg)](https://gitlab.electrocnic.com/dood/app/commits/master)
[![coverage report](https://test.gitlab.electrocnic.com/gitlab-badges/coverage.svg)](https://gitlab.electrocnic.com/dood/app/commits/master)
[![webpack version](https://test.gitlab.electrocnic.com/gitlab-badges/webpack_version.svg)](https://www.npmjs.com/package/webpack)
[![vue version](https://test.gitlab.electrocnic.com/gitlab-badges/vue_version.svg)](https://www.npmjs.com/package/vue)
[![django version](https://test.gitlab.electrocnic.com/gitlab-badges/django_version.svg)](https://www.djangoproject.com/download/)
[![nginx version](https://test.gitlab.electrocnic.com/gitlab-badges/nginx_version.svg)](https://docs.nginx.com/nginx/admin-guide/installing-nginx/installing-nginx-open-source/)
[![postgres version](https://test.gitlab.electrocnic.com/gitlab-badges/postgres_version.svg)](https://www.postgresql.org/download/linux/ubuntu/)
[![lighthouse performance](https://test.gitlab.electrocnic.com/gitlab-badges/performance.svg)](https://test.gitlab.electrocnic.com/gitlab-badges/report.html)
[![lighthouse accessibility](https://test.gitlab.electrocnic.com/gitlab-badges/accessibility.svg)](https://test.gitlab.electrocnic.com/gitlab-badges/report.html)
[![lighthouse best practices](https://test.gitlab.electrocnic.com/gitlab-badges/best_practices.svg)](https://test.gitlab.electrocnic.com/gitlab-badges/report.html)
[![lighthouse search engine results ranking](https://test.gitlab.electrocnic.com/gitlab-badges/search_engine_results_ranking.svg)](https://test.gitlab.electrocnic.com/gitlab-badges/report.html)
[![pip dependencies](https://test.gitlab.electrocnic.com/gitlab-badges/outdated_pip.svg)](https://test.gitlab.electrocnic.com/gitlab-badges/outdated.html)
[![npm dependencies](https://test.gitlab.electrocnic.com/gitlab-badges/outdated_npm.svg)](https://test.gitlab.electrocnic.com/gitlab-badges/outdated.html)


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
