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


# Vue-Django CI/CD template using GitLab, Cypress and Django Unit Tests and Docker
## What is this?

This is a Gitlab Boilerplate Vue-Django App to test frontend and backend unit- and integration-tests automated on a CI/CD system.
It is based on https://github.com/NdagiStanley/vue-django.git and meant to provide a boilerplate for continuous integration and continuous deploy.

I wanted to be able to deliver my web-applications in time with no/minimal bugs, and learned from the last month before a delivery (where I had no CI/CD setup yet), that this can make huge headaches.
Things were working on Windows but not on Linux anymore and the effort to fix that was days.
After it worked on linux, however, it did not work on the production server (also linux), because I did not start the app locally with the nginx-docker setup with https, I only ran it on my local machine with the `./deploy.sh` script.
Luckily, I was able to deliver in the last minute, but I don't want to repeat this again, so I began with this project.

Be aware, that a "meaty" "template" like this one has the disadvantage, that I chose most of the technologies forehand.
So if you like to use this template, I recommend you read the list of main-frameworks and technologies, on which it is based:
* Gitlab + Gitlab-Runner
* Vue (+vuex, +bootstrap-vue, +axios, ...)
* Django (python3)
* Webpack 4+
* Node/NPM
* Docker
* Docker-Compose
* nginx
* postgres

These technologies are more or less "deeply" integrated into the project and cannot be simply exchanged (but they can, if one does some effort, of course).
Further I use
* Cypress.io for frontend and integration tests
* nose for backend tests
* gunicorn for the connection between nginx and django
* nginx-proxy by jwilder (https://github.com/jwilder/nginx-proxy), which allows us hosting more than one app with different domains on the same machine with this CI/CD setup.

## TL;DR

This is for you, if you want to start with the development of a Vue-Django Webapp, with the benefits of a completely pre-configured gitlab CI/CD setup.
This is ONLY for you, if you are OK with the listed technologies above. Else, you can experiment and try to replace one technology with another, but no guarantees that it will work!


## Prerequesites

If you want to use this boilerplate you need at least:
1. A **gitlab runner in privileged mode** (needed for the docker-runner to be able to build and start more docker containers)
2. A **(private) docker registry** (if you run a private gitlab server instance, gitlab also provides a docker registry, or else you could use the public docker hub for example, if you don't care about your app being publicly available, but I don't recommend that as you will likely not want to share the secret keys which get embedded into the docker images when they are built)
3. A **production server** (A server instance where you want to deploy your app(s). Therefore, you need the IP address of that server) (Gitlab Variable: `DEPLOY_SERVER_IP`)
4. A **user named `gitlab` on your production server** which is in the `docker` group (`sudo gpasswd -a gitlab docker`)
5. A **public/private-key-pair (rsa):** Add the public key to the `authorized_keys` of your `gitlab` user on your deploy-server and add the private key (the content of the key-file) as String to the Gitlab-Variable `DEPLOY_SERVER_PRIVATE_KEY` under `Settings -> CI/CD -> Variables` and set the `Type` of the Variable to `File`
![Private Key Variable in Gitlab UI](documentation/media/private_key_variable.png?raw=true)
6. **`docker` and `docker-compose`** must be installed on the production server. I also highly recommend using Ubuntu on x86 for the server, I did not test the setup on `ARM` nor can I guarantee anything on a different environment.
7. **2 domains**: One **production domain**, where your app will finally be available to the public, and one **test-domain**, which is currently also available to the public, because I did not implement VPN for this purpose yet, but I am sure you can set it up yourself if you need a VPN for testing. The test domain is meant to be available from everywhere but not shared or advertised, so only you will know the URL. Examples: For the development of this boilerplate App I used the domains `production.gitlab.electrocnic.com` and `test.gitlab.electrocnic.com`. Currently they will both be deployed to the same IP, if you need to deploy them to two different IPs, just add another IP-Variable and use that variable in the `.gitlab-ci.yml`
The Variables for the domains should be added to the CI/CD Variables settings in Gitlab as well and are named `PRODUCTION_DOMAIN` and `TEST_PRODUCTION_DOMAIN`

## Installation/Setup

1. Fork or clone the repo. You will likely want to setup your own repo, I will skip the instructions of how to do this. (see https://stackoverflow.com/questions/18200248/cloning-a-repo-from-someone-elses-github-and-pushing-it-to-a-repo-on-my-github for example)
2. When you added a new empty gitlab-repo as the remote origin to your new local git repo from step 1, push it. The pipeline should be triggered but should fail.
3. Setup your gitlab account for that repo:
	* Add the following variables to your gitlab CI/CD Settings (all but the private key are of Type `Variable`):
		- `CERTBOT_EMAIL` (Your email address for certbot, optional)
		- `DEPLOY_SERVER_IP` e.g. `123.45.678.9`
		- `DEPLOY_SERVER_PRIVATE_KEY` (Type: `File`) paste the content of your private key as String
		- `DJANGO_DATABASE_HOST` e.g. `database1`
		- `DJANGO_DATABASE_NAME` e.g. `database1`
		- `DJANGO_DATABASE_PASSWORD` (Masked: `true`) a good password for your postgres instance (mine are 30 chars long and randomly generated using Enpass)
		- `DJANGO_DATABASE_USERNAME` e.g. `postgres_django`
		- `DJANGO_SECRET_KEY` (Masked: `true`) a good secret key for your django instance (mine is 50 chars long, as somebody stated in a Stackoverflow answer somewhere, that Django Secret keys should always be exactly 50 characters, and also randomly generated using Enpass)
		- `DOCKER_REGISTRY` The domain to your docker registry (mine was of my gitlab instance, e.g. `docker.gitlab.electrocnic.com`)
		- `DOCKER_PW` (Masked: `true`) the login credential to your docker registry
		- `DOCKER_USER` the user of your docker registry to which the password belongs
		- `PRODUCTION_DOMAIN` the domain under which you want to deploy your app. Note, that the app will be deployed using the `DEPLOY_SERVER_IP`, but this domain will be used for nginx to deliver the app when requests are made with that domain. Therefore, you have to make a DNS entry on your domain-provider to make it point to `DEPLOY_SERVER_IP`
		- `TEST_PRODUCTION_DOMAIN` the domain under which you want to deploy your test app. It is the same as the production app, but has its own gitlab jobs and docker images. This is to provide you a way to manually review your deployed app, before you actually update the production app.
		![Variables in Gitlab UI](documentation/media/all_variables.png?raw=true)
4. Edit the URLs in this README.md for the badges. Yes! You can re-use the badges, because they are meant to be part of the project!
You just have to use your `TEST_PRODUCTION_DOMAIN` for the svg badge-links (but hardcoded as the readme sadly does not substitute any variables). Just replace each occurrence of `test.gitlab.electrocnic.com` with your own `TEST_PRODUCTION_DOMAIN`. The badges will be created during the CI pipeline-jobs and will be deployed together with the test-instance (but not with the production instance). Lighthouse performance analysis will be ran and the badges will show the result and link to a in-depth lighthouse-report. Isn't that great?
5. Add a runner to your gitlab instance under `Settings -> CI/CD -> Runners`.
There you need to copy the runner token and configure a new runner on your private server where you host your gitlab runners, or maybe it is even possible to use a public gitlab.com shared runner, but I definitely do NOT recommend that, because you don't want to expose your secret keys and database password to any public instance.
I did not work with Kubernetes yet, so I have no idea if you could work with that or not.
If you add a specific runner manually, like I used it for this project, configure the runner with privileged mode!
For example I registered my new runner for this project with the following command (on a different server than on which my gitlab instance is running):
`sudo gitlab-runner register -n --url https://YOUR_GITLAB_DOMAIN/ --registration-token YOUR_SETTINGS_CI_CD_RUNNERS_REGISTRATION_TOKEN --executor docker --description "YOUR DESCRIPTION" --docker-image "docker:stable" --docker-privileged`
6. When you carefully followed them instructions, you can now commit your README.md, push it, and watch the first pipeline running. It may take quite some minutes per job (e.g. ~30 minutes for the first job to build the base images for the first time, they will be re-used for future jobs, but updated every time you add pip or npm packages)
7. You can now also add your first tag (git tag) either with git manually or on gitlab `Repository -> Tags -> New Tag`. A new tag will trigger the tagged pipeline and will therefore build the test and production images and will deploy the test app to your production server. The configuration is by intention, that you have to trigger the production-deploy by hand (after you added a new tag), to avoid unintentional headaches.
8. I highly recommend to add a scheduled pipeline on your master branch in gitlab under `CI/CD -> Schedules -> New schedule` on a `daily` basis, which will then update the badges daily, so they show up-to-date information about outdated packages and so on.
9. You should be able to visit your deployed sites under the domains you provided for the variables. The production domain should only accept https, whilst the test domain should accept both, https and http (but will likely automatically always redirect to https).
10. **IMPORTANT:** The very first registered user will become a Admin user on django. Therefore, as soon as you deployed your production app, you should register your admin (superadmin) user at the endpoint `YOUR_DOMAIN/api/v1/auth/register/`.
Then you can login at `YOUR_DOMAIN/admin/`. Each user who will register from now on has no special privileges and cannot visit `/admin/`, but can be made `staff` or `admin` by the first Admin.

## Local execution

Locally, you need a global installation of `npm` and `python3` and then you should be able to simply execute `./deploy.sh` which should do all the preparation for you on a first-time run and it should work on Linux as well as on Windows in the Git Bash.
This does not start or build any docker containers or images, it just builds the Vue-App and runs a Django-Server, so you should be able to reach your app on `localhost:8000` when you keep the process open.

If you only want to quickly build and test the frontend only, `cd client` and `npm run dev`. The app should be visible at `localhost:8080`.
Currently, I did not add any helper scripts which build the docker images locally. However, you can always run a normal commit-pipeline (not a tagged one) which will build and push debug-images, which are meant to serve the app at `localhost:8000`, so if you want to locally run the app with docker-compose, you would need to `docker pull YOUR_DOCKER_REGISTRY_DOMAIN/YOUR_GITLAB_PROJECT_PATH/app:latest` (+`.../nginx:latest`, +`.../postgres:latest`)
and run it with a modified `docker-compose.yml` (or export the variable which are used by `docker-compose.yml` in the shell beforehand).


## Continuous Deploy Overview (CD)
![Production workflow](documentation/media/overview_01.svg?raw=true)

This minimalistic sketch should provide a quick overview of how the CI/CD setup is designed: Each project based on this boilerplate will build the docker images `app`, `nginx` and `postgres` and will use the publicly available docker images of jwilder's nginx-proxy `nginx`, `jwilder/docker-gen` and `jrcs/letsencrypt-nginx-proxy-companion`.
The Latter 3 are combined in a docker-compose setup which will be started only once for all projects on that server. (The deploy job will care about that).
Your app's images come in 3 flavors:
* `image:latest` - The debug images with public exposed domain `localhost:8000` and not https support.
* `image:TAG-test` - The test images with the version from your last git tag and a "-test" postfix with https support and the domain being `TEST_PRODUCTION_DOMAIN`
* `image:TAG` - The production images with the version from your last git tag and nothing else, with https only and the domain being `PRODUCTION_DOMAIN`

Behind the scenes there are two additional docker images being built, used and pushed to your registry:
1. The `debian-dind:latest` image, which is a custom debian based Docker image with dind-support, because the official dind images are not based on debian or ubuntu and then there is no `apt` which I personally find pretty annoying.
2. The `builder:latest` image, which is the image used for all of the job-runners.
This image acts as a cache for your npm and pip dependencies, in order to avoid them being downloaded on every pipeline again. If you update your `package.json` or your `requirements.txt` or if you change the Dockerfile, the `update-base-image` job will update these images.

#### Deploy

The deploy process will simply copy the latest `docker-compose.yml` of the folder `deploy/app/` with `scp` to your server and will then run `docker-compose pull && docker-compose up` to update the images of the app to the new version and to start it again with the new version. (This explanation is simplified, there is more fidelity behind the scenes, which you can see when you look at the deploy scripts).
The deploy process will also first copy the `docker-compose.yml` of the `nginx-proxy` if the nginx-proxy is not running yet on the remote host.
The `nginx-proxy` will automatically detect new apps as soon as the app starts and will have a common docker-network with all apps (which are configured for that purpose) and will automatically update the letsencrypt certificates for the newly started app.
So in a few seconds to minutes after the deploy has finished, the app should be reachable with https.
Volumes of your app remain on updates, if you do not change any keys or names in the docker-compose files. If any volume name or service name changes, docker-compose might have struggles with the database volume from the previous version and you might not be able to deploy the new version without forcefully clear your database (which you would have to do by hand, so no panic).
Each update should also trigger a `python manage.py migrate` on your production (and test) instance, so that the database scheme gets its updates as well.

This boilerplate is meant to be as focused as possible to the simple use case where a single developer wants to make a Vue/Django App and the requirements are not too high. Thus, I did not plan any decoupling for the database, but, if you set every variable and every setting correctly, you can for sure use externally hosted databases and different database services than postgres as well. Please just don't expect any support by me.

## Continuous Integration (CI)

The CI pipeline is designes as following:

1. `update-base-image` - The images `debian-dind` and `builder` get checked if updates are needed and will eventually be updated. An update might take 15 to 30 minutes. If no update is needed, this job should finish within 4 minutes.
2. `build-images` - aka "verify-build" will build the app and run django nose tests. The coverage result only depends on the output of these tests, as I did not add coverage for frontend tests. Here, the three images `app:latest`, `nginx:latest` and `postgres:latest` are created and pushed to the docker registry you configured in the gitlab variables.
3. `run-tests` - The app will be run in debug mode and frontend/integration tests will be run with cypress. If cypress fails, the pipeline fails. This is also a great indicator if your webpack configuration and your staticfiles/routes/paths/api works: If something is wrong with the staticfiles or so, cypress will likely not be able to display the page and will fail.
4. `test-release` and `release`: The release images will be built. The only reason why they will be built in seperate jobs are slightly different configuration parameters which get embedded into the docker images during the `docker build` command. However, the benefits are that you have images with extinct tags for each type of app and cannot easily deploy a debug version to your production server by mistake.
5. `test-deploy` and `deploy`: The app will be deployed on the production server. The `deploy` job needs to be triggered manually for safety reasons. When this stage succeeds, the app should be visible to the public with https.
6. `create_badges`: The last job after `test-deploy` which will run analysis against your test server and will upload the reports to a publicly available but non-obvious URL on your test-server. The reports are available through a click on the badges.
7. `update_dependency_badges`: This job has to be scheduled via `CI/CD -> Schedules -> New schedule` in your gitlab instance. It should be scheduled on a daily basis to keep the dependency-badges up-to-date.

## Project Setup / Development

You will basically almost never need to touch any directories other than `backend` and `client`.
The Django source code is in `backend`, the Vue source code and the webpack configuration is in `client`.
The virtualenv (`.venv`) will be created in `backend` and the `node_modules` will be cached in `client`.
You will likely very often want to call `./deploy.sh` from the project's root directory, and `npm run dev` from the projects `client` directory.
You can also run `python manage.py runserver` from `backend`, but be aware that you `source .venv/bin/activate` or `source .venv/Scripts/activate` before you do that in `backend`.
You can also run django nose tests with `python manage.py test` in the `backend` directory.

Here is a short overview of what commands are useful on your local machine:

| (`cd` into) Directory | Script/Command | Info |
|------|------|-------|
| `project-root/` | `./deploy.sh` | Will build and then run the app.<br>Also installs all missing node modules and pip dependencies<br>and creates a new `backend/.venv` (pip-virtualenv) directory,<br>if it does not exist yet. |
| `project-root/` | `./deploy.sh run` | Will skip a rebuild and will only start<br>the Django server to run the app.<br>With both commands, you should be able to<br>reach your App in a Webbrowser with<br>the URL `localhost:8000` |
| `project-root/util/` | `./hard_reset_db.sh` | Will delete all migration folders<br>which are defined in this script (you are<br>responsible to add them to the script if you want to use<br>this script and if you add new Django apps),<br>and deletes the `db.sqlite3` file,<br>then runs new migrations from scratch,<br>so you have a fresh and empty database<br>with your latest db-scheme.<br>This often helps during development<br>to get rid of some annoying db-scheme-constellations,<br>which can occur quite often during the<br>early phase of dev, but in this phase<br>you likely won't care about losing data. |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

<!-- TODO: Add description of webpack config, Vue src code, api/axios, django router+vue-router and django setup and config -->

... More is coming...

## More

For a detailed explanation on how things work, check out the [guide](http://vuejs-templates.github.io/webpack/) and [docs for vue-loader](http://vuejs.github.io/vue-loader).


