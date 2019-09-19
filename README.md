<!-- Badges are (except for pipeline status and coverage report) created in util/run_lighthouse.sh, there they will also be uploaded to the URLs listed below. -->
[![version](https://test.odpr.electrocnic.com/gitlab-badges/latest_release_tag.svg)](https://gitlab.com/electrocnic/vue-django-ci-cd-boilerplate/commits/master)
[![pipeline status](https://gitlab.com/electrocnic/vue-django-ci-cd-boilerplate/badges/master/pipeline.svg)](https://gitlab.com/electrocnic/vue-django-ci-cd-boilerplate/commits/master)
[![coverage report](https://test.odpr.electrocnic.com/gitlab-badges/coverage.svg)](https://gitlab.com/electrocnic/vue-django-ci-cd-boilerplate/commits/master)
[![webpack version](https://test.odpr.electrocnic.com/gitlab-badges/webpack_version.svg)](https://www.npmjs.com/package/webpack)
[![vue version](https://test.odpr.electrocnic.com/gitlab-badges/vue_version.svg)](https://www.npmjs.com/package/vue)
[![django version](https://test.odpr.electrocnic.com/gitlab-badges/django_version.svg)](https://www.djangoproject.com/download/)
[![nginx version](https://test.odpr.electrocnic.com/gitlab-badges/nginx_version.svg)](https://docs.nginx.com/nginx/admin-guide/installing-nginx/installing-nginx-open-source/)
[![postgres version](https://test.odpr.electrocnic.com/gitlab-badges/postgres_version.svg)](https://www.postgresql.org/download/linux/ubuntu/)
[![lighthouse performance](https://test.odpr.electrocnic.com/gitlab-badges/performance.svg)](https://test.odpr.electrocnic.com/gitlab-badges/report.html)
[![lighthouse accessibility](https://test.odpr.electrocnic.com/gitlab-badges/accessibility.svg)](https://test.odpr.electrocnic.com/gitlab-badges/report.html)
[![lighthouse best practices](https://test.odpr.electrocnic.com/gitlab-badges/best_practices.svg)](https://test.odpr.electrocnic.com/gitlab-badges/report.html)
[![lighthouse search engine results ranking](https://test.odpr.electrocnic.com/gitlab-badges/search_engine_results_ranking.svg)](https://test.odpr.electrocnic.com/gitlab-badges/report.html)
[![pip dependencies](https://test.odpr.electrocnic.com/gitlab-badges/outdated_pip.svg)](https://test.odpr.electrocnic.com/gitlab-badges/outdated.html)
[![npm dependencies](https://test.odpr.electrocnic.com/gitlab-badges/outdated_npm.svg)](https://test.odpr.electrocnic.com/gitlab-badges/outdated.html)

# ODPR - Open Database for Physically Based Rendering

A Vue-Django Webapp to provide user-provided scenes (3D Models and sceneries) for the public use.

# vue-django-ci-cd-boilerplate

## Content

1. [What is this?](#what-is-this)
2. [TL;DR](#tldr)
3. [Prerequisites](#prerequisites)
	1. [Docker Credential Store on Production Server](#docker-credential-store-on-production-server)
4. [Installation/Setup](#installationsetup)
5. [Local execution](#local-execution)
6. [Continuous Deploy Overview (CD)](#continuous-deploy-overview-cd)
	1. [Deploy](#deploy)
7. [Continuous Integration (CI)](#continuous-integration-ci)
8. [Project Setup / Development](#project-setup-development)
	1. [Django router + Vue router + URLs - how does all of that work?](#django-router-vue-router-urls-how-does-all-of-that-work)
	2. [Server (Django) (Backend)](#server-django-backend)
	3. [Client (Vue) (Frontend)](#client-vue-frontend)
9. [Variable Injections](#variable-injections)
10. [Security](#security)
11. [Useful Links](#useful-links)
12. [Contribution](#contribution)
13. [Feature-List](#feature-list)
14. [FAQ / Troubleshooting](#faq-troubleshooting)
	1. [CI Build problems](#ci-build-problems)
	2. [Deploy problems](#deploy-problems)
	3. [Local Build problems](#local-build-problems)
	4. [OS and environment](#os-and-environment)
15. [Uninstall](#uninstall)
	1. [Uninstall App only](#uninstall-app-only)
	2. [Uninstall all apps + nginx-proxy](#uninstall-all-apps-nginx-proxy)


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


## Prerequisites

If you want to use this boilerplate you need at least:
1. A **gitlab runner in privileged mode** (needed for the docker-runner to be able to build and start more docker containers)
2. A **(private) docker registry** (if you run a private gitlab server instance, gitlab also provides a docker registry, or else you could use the public docker hub for example, if you don't care about your app being publicly available, but I don't recommend that as you will likely not want to share the secret keys which get embedded into the docker images when they are built)
3. A **production server** (A server instance where you want to deploy your app(s). Therefore, you need the IP address of that server) (Gitlab Variable: `DEPLOY_SERVER_IP`)
4. A **user named `$DEPLOY_SERVER_USER` on your production server** which is in the `docker` group (`sudo gpasswd -a DEPLOY_SERVER_USER docker`). Set the `DEPLOY_SERVER_USER` as a variable in the gitlab settings.
5. A **public/private-key-pair (rsa):** Add the public key to the `authorized_keys` of your `DEPLOY_SERVER_USER` user on your deploy-server and add the private key (the content of the key-file) as String to the Gitlab-Variable `DEPLOY_SERVER_PRIVATE_KEY` under `Settings -> CI/CD -> Variables` and set the `Type` of the Variable to `File`
![Private Key Variable in Gitlab UI](documentation/media/private_key_variable.png?raw=true)
6. **`docker` and `docker-compose`** must be installed on the production server. I also highly recommend using Ubuntu on x86 for the server, I did not test the setup on `ARM` nor can I guarantee anything on a different environment.
7. **2 domains**: One **production domain**, where your app will finally be available to the public, and one **test-domain**, which is currently also available to the public, because I did not implement VPN for this purpose yet, but I am sure you can set it up yourself if you need a VPN for testing. The test domain is meant to be available from everywhere but not shared or advertised, so only you will know the URL. Examples: For the development of this boilerplate App I used the domains `production.gitlab.electrocnic.com` and `test.gitlab.electrocnic.com`. Currently they will both be deployed to the same IP, if you need to deploy them to two different IPs, just add another IP-Variable and use that variable in the `.gitlab-ci.yml`
The Variables for the domains should be added to the CI/CD Variables settings in Gitlab as well and are named `PRODUCTION_DOMAIN` and `TEST_PRODUCTION_DOMAIN`

### Docker Credential Store on Production Server

You might want to configure a docker-credential-store to prevent docker from storing your docker-password in plain-text in the docker-config file.
For now, this is basically irrelevant, as the docker password is stored in plain-text in the app's startscript `app.sh`.
However, if you want to configure it, here is a step-by-step solution for Ubuntu, copied from [here](https://github.com/docker/docker-credential-helpers/issues/102#issuecomment-388634452):
1. `wget https://github.com/docker/docker-credential-helpers/releases/download/v0.6.3/docker-credential-pass-v0.6.3-amd64.tar.gz`
2. `tar -xf docker-credential-pass-v0.6.3-amd64.tar.gz`
3. Copy unpacked file(s) to `/usr/bin` or configure `$PATH` to add its current location.
4. Check that docker-credential-pass works by running `docker-credential-pass`. You should see: `Usage: docker-credential-pass <store|get|erase|list|version>`.
5. `sudo apt update && sudo apt install gpg pass`
6. `gpg --generate-key`. Enter your name, mail, etc. You will get gpg-id (pub) like "5BB54DF1XXXXXXXXF87XXXXXXXXXXXXXX945A". Copy it to clipboard. The command will likely hang if you are in a remote-ssh terminal session. Therefore: Open a second ssh connection and run: `sudo dd if=/dev/nbd0p1 of=/dev/zero` which will result in disk-usage while gpg calculates random numbers. Stop this second command when gpg has finished. Instead of `/dev/nbd0p1` you should be able to use any existing device listed under `ls /dev`.
7. `pass init KEY_FROM_CLIPBOARD`
8. `pass insert docker-credential-helpers/docker-pass-initialized-check` and set the password to `pass is initialized`.
9. `pass show docker-credential-helpers/docker-pass-initialized-check` and the output should be `pass is initialized`.
10. `docker-credential-pass list` should either output `{}` or some data but no error.
11. `vim ~/.docker/config.json` (from the user where the docker-config json is stored) and set in root node the next line `"credsStore": "pass"`
12. `docker login` should work now and the password should not be stored in plain text in the `~/.docker/config.json`.

## Installation/Setup

1. Fork or clone the repo. You will likely want to setup your own repo, I will skip the instructions of how to do this. (see https://stackoverflow.com/questions/18200248/cloning-a-repo-from-someone-elses-github-and-pushing-it-to-a-repo-on-my-github for example)
2. When you added a new empty gitlab-repo as the remote origin to your new local git repo from step 1, push it. The pipeline should be triggered but should fail.
3. Setup your gitlab account for that repo:
	* Add the following variables to your gitlab CI/CD Settings (all but the private key are of Type `Variable`):
		- `CERTBOT_EMAIL` (Your email address for certbot, optional)
		- `DEPLOY_SERVER_IP` e.g. `123.45.678.9` (should also be possible to use a domain instead as it is used for ssh and scp)
		- `DEPLOY_SERVER_USER` e.g. `gitlab`. The user must exist on the deploy server and the public key must be added to the `authorized_keys`.
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
		- `PROXY_SERVER_IP` Optional: If you cannot ssh to your deploy server directly but need to connect to an intermediate server instead, use this extra variable.
		- `PROXY_SERVER_USER` Optional: Use this if you also use `PROXY_SERVER_IP`. The user with which gitlab will try to login to the proxy server.
		- `PROXY_SERVER_PRIVATE_KEY` Optional: Use this if you also use `PROXY_SERVER_IP`. The private key which is accepted by `PROXY_SERVER_USER` on the server `PROXY_SERVER_IP`. The corresponding public key needs to be added to the `authorized_keys` of the proxy server.
		![Variables in Gitlab UI](documentation/media/all_variables.png?raw=true)
		(Important: Not all variables are shown in the screenshot)
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
|---|---|---|
| <nobr>`project-root/`</nobr> | <nobr>`./deploy.sh`</nobr> | Will build and then run the app. Also installs all missing node modules and pip dependencies and creates a new `backend/.venv` (pip-virtualenv) directory, if it does not exist yet. |
| <nobr>`project-root/`</nobr> | <nobr>`./deploy.sh run`</nobr> | Will skip a rebuild and will only start the Django server to run the app. With both commands, you should be able to reach your App in a Webbrowser with the URL `localhost:8000` |
| <nobr>`project-root/util/`</nobr> | <nobr>`./hard_reset_db.sh`</nobr> | **WARNING** This will delete all your data in your local database! Will delete all migration folders which are defined in this script (you are responsible to add them to the script if you want to use this script and if you add new Django apps), and deletes the `db.sqlite3` file, then runs new migrations from scratch, so you have a fresh and empty database with your latest db-scheme. This often helps during development to get rid of some annoying db-scheme-constellations, which can occur quite often during the early phase of dev, but in this phase you likely won't care about losing data. |
| <nobr>`project-root/backend/`</nobr> | <nobr>`source .venv/bin/activate` (Linux)</nobr> `source .venv/Scripts/activate` (Windows) | Needed, for all python commands below. Will set pip and python paths to your `.venv` directory. |
| <nobr>`project-root/backend/`</nobr> | <nobr>`python manage.py test --attr='assertAlmostEqual'`</nobr> | `source .venv/bin/activate` or on Windows: `source .venv/Scripts/activate` is needed before you can run this command! Without `--attr='assertAlmostEqual'` nose will not be intelligent enough to run tests only on TestClasses. It will also run tests on every single helper/util method which is in a test-file. Also, if you are on Linux, `python` might not work, try `python3` instead. This command will only test your backend with a virtual in-memory-database, which is created during this command and destroyed at the end of the tests. |
| <nobr>`project-root/backend/`</nobr> | <nobr>`python manage.py makemigrations`</nobr> | `source .venv/bin/activate` or on Windows: `source .venv/Scripts/activate` is needed before you can run this command! Everytime to change your Django models or add new Django Apps or pip dependencies, you will likely want to run this command. It will create or update the content of the `migrations` folders in your apps and in your dependencies. After this command, you will also most likely want to run `python manage.py migrate` which will then use the updated information of your migrations-folders and apply them on your database file/instance (`db.sqlite3`). |
| <nobr>`project-root/backend/`</nobr> | `python manage.py makemigrations <app1> <app2> <app_n>` | `source .venv/bin/activate` or on Windows: `source .venv/Scripts/activate` is needed before you can run this command! Sometimes, the above command does not make migrations for individual apps for some reason. Here you can go sure that it will update the migrations for specific apps. |
| <nobr>`project-root/backend/`</nobr> | <nobr>`python manage.py migrate`</nobr> | `source .venv/bin/activate` or on Windows: `source .venv/Scripts/activate` is needed before you can run this command! After the above 2 commands, you will also most likely want to run this command which will then use the updated information of your migrations-folders and apply them on your database file/instance (`db.sqlite3`). |
| <nobr>`project-root/backend/`</nobr> | <nobr>`python manage.py createsuperuser`</nobr> | `source .venv/bin/activate` or on Windows: `source .venv/Scripts/activate` is needed before you can run this command! When you have a fresh database, you might want to create a new admin user for your django app, in order to be able to test the app manually on `localhost:8000/admin/`. In this boilerplate I provide a way to add a superuser even in production (because you will definitely want to have at least one admin in production as well, but `python manage.py createsuperuser` is no longer possible in production, thus the first registered user will automatically become a superuser. (`localhost:8000/api/v1/auth/register/`) |
| <nobr>`project-root/client/`</nobr> | <nobr>`npm run build`</nobr> | Will build the Vue app. This means, npm will use the configuration of `project-root/client/package.json` and will run webpack with its configurations from `project-root/client/build/` and `project-root/client/config`. Webpack will then resolve all node_modules and asset-dependencies (.js, .css, .sass, .png, etc) and will create so-called chunks of your bundled app. It will inject the start-point (a few files (chunks) that represent the "entrypoint") into the main `index.html` file. This command is used when you want to be able to test your full app: Frontend WITH Backend. This command is also already used by the `./deploy.sh` script. |
| <nobr>`project-root/client/`</nobr> | <nobr>`npm run dev`</nobr> | Will build the Vue app with a few different settings and modes and will immediately start an integrated server to serve the static frontend at `localhost:8080`. It also provides more detailed build-error-messages than `npm run build` and is faster. Useful only if you only want to view your Frontend changes without the need for a connected backend. This command is also most likely what you will want to keep opened in a terminal while developing Vue: It auto-updates on file-changes and displays the changes immediately in the browser without the need for manual page-reloads. |
| <nobr>`project-root/client/`</nobr> | <nobr>`npm run test`</nobr> | Will start cypress and will run your frontend and integration tests using cypress. For this command to work properly, you will need to open a second terminal where you run `./deploy.sh`, because cypress runs its tests against the full app, and not against the static frontend only (as it is configured currently). |

### Django router + Vue router + URLs - how does all of that work?

1. User requests the site `https://example.com`
2. nginx-proxy looks if any app with a running nginx server with this domain is listening and passes the request through to this app.
3. the nginx server in the app passes the request through gunicorn to Django
4. Django trys to match the request URL with the api-urls in the urls.py
5. For the main page with no additional patterns, Django will find the URL `/` matching and will return the mapped index.html.
6. If a user makes another request, for example `https://example.com/subpage1`, where the additional pattern `subpage1` occurs,
	**Django** will no more longer match the incoming URL with `/`, but will try to find another matching entry.
	1. If found,
	Django will call the class/method/instructions mapped to the matching URL. E.g. `example.com/admin/` matches a third-party-library
	endpoint url and Django will return pre-rendered backend UI pages, so the user is able to navigate through sites solely created
	by Django where our Vue-frontend is never even touched.
	2. If NOT found, Django will execute the defined fallback mechanism,
	which could for example be to return a `404 not found` page, or, in our case, the instruction to just return the `index.html`
	like we did at the main-page-URL `/`, but this time, Django will also pass the request URL through to Vue, so we load `index.html`,
	render Vue, and let our **vue-router** decide what to do with the URL:
		1. It's the same game again: If the URL matches a pattern
	defined in our Vue-Router, the router will navigate to that (sub)-page or perform any code which is mapped to the URL-pattern.
		2. If NOT found, you can again decide, if you want to display a beautiful-vue-rendered `404 Not Found` or if you just want to
	kick the user back to the beginning - The main page `example.com`.
	![Routes workflow](documentation/media/routes_03.svg?raw=true)


### Server (Django) (Backend)

I won't go into depth of how Django works. You need to read the official Django Docs and find other tutorials for that.
Also, take care, that the Django-Rest-Framework is a third-party library, something like a "plugin" if you want to call it so,
which is needed in order to be able to have a custom frontend framework as your client like Vue, React, Angular, etc.
Else, Django is meant to directly serve and render your frontend as well ("Server side rendering"), but you want to build
an App with cool stuff, so you don't want server-side-rendering, alright?

However, here's still a short overview:

The main config for django lies in `backend/vuedj/settings.py` and in the same folder is the crucial `urls.py` where all subsequent
url-patterns have their "entrypoint".

There are 4 custom apps installed already, as part of this boilerplate (but in addition to them there are many more third-party apps
defined in `settings.py`): Those are
* **accounts** - All about user registration and login/register/pw-reset etc. (Also the crucial admin is handled here, so if you don't plan to
enable user-registration at all, you might at least want access to your backend configuration in production as admin-user)
* **api** - This is an intermediate layer to keep your api clean and easy to maintain. This app does nothing but including all of YOUR apps into
its `api/urls.py` which is itself just once included in the main `vuedj/urls.py`. This is to avoid a huge and bloated `vuedj/urls.py`.
* **app** - The main app of your backend. Which is empty for now, but you might want to begin here (or in `accounts`) to develop your backend.
* **test_util** - Also not really an "app", it's just there to provide a way to gather common helper classes and helper methods for your backend tests.
You might want to have a look at them and use them now or then.

### Client (Vue) (Frontend)

There are a lot of folders and files in the `client` directory: Most of them are configuration files for webpack, eslint,
babel, npm, or their output directories. You will most likely rarely need to touch the files in `config`, `build` or
`package.json`, but you WILL. For example, you should update the information in `package.json` to your needs, currently
there is meta information of the boilerplate included which you don't want to keep with you.

If you add any additional npm packages, you will likely want to update the `build/webpack.prod.conf.js` to add the new
libraries and configure them with webpack.

If you want to write frontend tests, the folder `cypress/integration` is your start-point. Minimal tests are already inside.
These tests are also already running on gitlab CI.

The actual development takes place in `src`. This is your playground.

The `format_index_html.py` is crucial and will overwrite the webpack-generated `templates/index.html` with some
dynamic instructions for static files. Static files are the files which represent your whole app when built.
You can imagine the `staticfiles`-directory (which will be in the project's root) being the "image" of your frontend.
All the files in the `staticfiles`-directory are somehow linked/referenced in the main `index.html`.
The main `index.html` is the end-result of the steps `npm run build` plus `python format_index_html.py` in the client
directory and is NOT the `client/index.html` but the `client/templates/index.html`. The `client/index.html` is the
source for webpack, which is needed in order to provide the first skeleton where webpack will inject links and
reference to the generated chunks (your actual Vue-App).
I also added a Preloader to the `client/index.html` consisting of plain css and javascript, which removes the preloader-DOM
as soon as the site is completely loaded. As a Single-Page-Application like this is one can become quite bulky for the
initial load, a Preloader is something you will very likely want to have (like jsfiddle.com has one for example)

## Variable Injections

You might notice that there are some environment variables in use in some of the config or even source files. Please
don't touch them, they are needed by the gitlab CI/CD setup, so you do not need to care about debug vs. production settings
AT ALL! They should solely be configured in `.gitlab-ci.yml` or even better in your Gitlab UI Settings.
For example such variables look like this in the code:
`process.env.APP_INDEX_HTML_TEMPLATE_DIRECTORY` in `client/config/index.js`
`os.getenv('DJANGO_SECRET_KEY')` in `backend/vuedj/settings.py`

## Security

Currently, the Django-Secret and the postgres password and postgres-username will get injected into the Docker-Image
during the image-build. They will stay there as environment variables. This might not seem like the best solution, so if
you have any suggestions to improve it feel free to open an issue or contribute.

The docker registry credentials (password, username, domain) will be saved HARDCODED on the DEPLOY-server in each app's
start-scripts, in order to be able to login to your docker registry and to update the app's images.

The secrets are never committed in the code though, so you will not expose them publicly if you do not expose the docker
images themselves in public.

https support is enabled per default and even forced in the production image, but completely handled by the third-party
nginx-proxy.

You should have a private docker registry and you should keep access to the repo private (or for trusted people) only.

## Useful Links

[Vue Documentation](https://vuejs.org/v2/guide/)<br>
[Vuex Documentation](https://vuex.vuejs.org/guide/)<br>
[Vue-Router Documentation](https://router.vuejs.org/)<br>
[CSS Guideline](https://cssguidelin.es/)<br>
[Django Documentation](https://docs.djangoproject.com/en/2.2/)<br>
[Django REST Framework Documentation and Tutorials](https://www.django-rest-framework.org/)<br>
[Webpack Documentation](https://webpack.js.org/concepts/)<br>
[npm Documentation](https://docs.npmjs.com/)<br>
[pip Documentation](https://pip.pypa.io/en/stable/)<br>
[pip Documentation](https://pip.pypa.io/en/stable/)<br>
[Gitlab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)<br>
[Docker and Docker-Compose Documentation](https://docs.docker.com/ee/)<br>
[nginx Documentation](http://nginx.org/en/docs/)<br>
[postgres Documentation](https://www.postgresql.org/docs/manuals/)<br>
[Basics of Bash Scripting (for beginners)](https://linuxconfig.org/bash-scripting-tutorial-for-beginners)<br>


## Contribution

You feel you can and want add some features or enhance some existing features?
You feel you could add more documentation?
Please feel free to ask for contribution permissions or open issues.

## Feature-List

A list of contained features below:

* Gitlab **CI configuration** for automated build and testing
* **Backend tests** in CI (with example test)
* **Frontend/Integration tests** in CI (with example test)
* Gitlab **CD configuration** as CI job
* **Production deployment** with automatic **https enforcement** (and **auto-update certificates**)
* **Test deployment** with https+http support (and auto-update certificates)
* **Debug images** with debug-configuration (Vue devtools, Django exceptions in browser, localhost:8000).
* **Badges** (You see them on top of this README) (they include **lighthouse analyzis**)
* **Preloader:** As a SPA (Single Page Application) might be very bulky very fast, the initial load can be slooooow.
An animated css-preloader for the frontend is already included in order to give a better impression for you customers.
It is included in the main `index.html` file directly.
* **Cookies Agreement popup.** Included in `App.vue`: Using [Vue Cookie Law](https://www.npmjs.com/package/vue-cookie-law).
* **Preconfigured Webpack:** Output in chunks, sass/scss support, bootstrap-vue and bootstrap included.
* **Bootstrap + Bootstrap-Vue**
* **axios:** A first simple api is already setup in Vue+Django in order to give you a starting point for the API.
* **Django + Django Restframework:** The restframework is already configured so, that you can test the accounts-urls.
* **Admin** on production server: First registered user becomes superadmin in django.
* **Multiple Apps** on one deploy-server: The nginx-proxy will automatically detect all apps which are deployed to the same
server using this boilerplate. The deploy mechanism will recognize if nginx-proxy is already up and running on the target.
* **Local Build** with `./deploy.sh`: This script supports Windows and Linux (tested on Ubuntu 18.04) and is a Zero-Config
except that you need to install npm and python3 on your system yourself before you can use it.
* **nginx gzip compression**: Static files are compressed with nginx on the fly. Webpack could be used with a plugin to
compress the files during build, but that will not work together with chunks, and chunks are more important, and nginx-compression
works very well.
* **preload-assets:** Preload the chunks in the `index.html` file.
* **Proxy-server for deployment:** If you cannot access your deployment server directly, but need to first ssh to an intermediate server,
you can add the optional variables `PROXY_SERVER_IP`, `PROXY_SERVER_USER` and `PROXY_SERVER_PRIVATE_KEY` to let the deploy job
first connect to your intermediate server and then to the deploy server. If not provided, the deploy job will directly connect to
the provided deploy-server ip and user.

## FAQ / Troubleshooting

### CI Build problems

1. Did you set all variables in `Gitlab -> Settings -> CI/CD -> Variables`?
2. Did you add a runner to your gitlab setup in privileged mode?
3. Did you add a valid docker registry url with valid docker registry credentials to the variables in Gitlab?

### Deploy problems

1. Did you create a `gitlab` user on your production server and did you add it to the docker-group?
2. Did you add the **CONTENT** of your private key file as a Variable **OF TYPE FILE** in gitlab?
3. Did you add the public key to the `authorized_keys` file of your gitlab-user on your deploy server?
4. Did you install docker and docker-compose on your production server?
5. Are all of the files and directories on the deploy server on `~/` owned by the gitlab user, or are (some of them) they
owned by root or any other user?

### Local Build problems

1. Delete the `project-root/staticfiles/*` content and the `project-root/client/static-vuedj` directory.
2. Look at the error messages of webpack and npm closely, **google them**.
3. Try to build with `cd client && npm run dev`, maybe it has more detailed error messages.
4. Is the variable you just used in the Vue-template-section a variable or a method?
5. Did you define the method as a function or as a dictionary/object by mistake?

### OS and environment

I used:
* Windows: Git-Bash + IntelliJ + WebStorm + PyCharm
* Ubuntu 18.04: gnome terminal + IntelliJ + WebStorm + PyCharm
* Ubuntu 18.04 on x86: For the production server for deployments.

I cannot help you if you use a different environment.


## Uninstall

### Uninstall App only

ssh to your production server with the gitlab-user and `~/apps/YOUR_APP_DOMAIN/app.sh stop` to gracefully stop the app
first. Then `rm -rf ~/apps/YOUR_APP_DOMAIN` and do that once for the
test-domain of that app and once for the production-domain.
Then delete the docker images which might still be around.
(`docker images` and `docker rmi IMAGE_ID_APP IMAGE_ID_APP_NGINX IMAGE_ID_APP_POSTGRES`)

### Uninstall all apps + nginx-proxy

Repeat the above process for all apps in `~/` on your deploy server and for the nginx-proxy use `~/nginx-proxy/nginx-proxy.sh stop` instead.
