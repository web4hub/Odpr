#!/bin/bash
#
# This script is meant to emulate a gitlab runner exactly on your local machine.
# Thus you do not have to setup a runner if you do not have a server.
set -eo pipefail

source util/local_docker_build/variables.sh

############### Build/Update Debian-Dind image in original docker:dind image ###########################################

# Step 1: Create docker cache for inside dind built images
mkdir -p /tmp/docker-cache

# Step 2: Start privileged docker container which has this project inside.
# mount the source readonly, so we can use it for the dependencies but cannot accidently corrupt the code.
# bind-mount the custom docker cache so we can keep the image we build inside.
docker run \
	--privileged \
	-d \
	-v "$(pwd)":/project:ro \
	--mount type=bind,source=/tmp/docker-cache,destination=/var/lib/docker \
	--name=dind \
	-i docker:dind 2>/dev/null \
	&& sleep 20 \
	|| docker start dind

# Step 3: Update or freshly build debian-dind image, which will be a base image for further use.
docker exec -i dind sh /project/debian-dind/update_dind_image_locally.sh


############### Build/Update Builder image in custom debian-dind image #################################################

# Step 4: Update or build the builder image which acts as a node_modules- and pip-cache.
docker exec -i dind sh /project/builder/update_builder_locally.sh

# Step 5: Stop the helper-dind.
docker stop dind


############### Build app/nginx/postgres images in the custom builder-container ########################################

# Step 6: Start privileged builder container with the cached node_modules and pip dependencies of the project.
# mount the source readonly, so we can use it for the compilation of the app, but cannot accidently corrupt the code.
# bind-mount the custom docker cache so we can keep the image we build inside.
docker run \
	--privileged \
	-d \
	-v "$(pwd)":/project:ro \
	--mount type=bind,source=/tmp/docker-cache,destination=/var/lib/docker \
	--name=builder \
	-i "${BUILDER_IMAGE}" \ # TODO: find out how to pass the complete path to this image as it cannot be found in the default cache.
	&& sleep 20 \
	|| docker start builder

# Step 7: Build app in builder.
docker exec -i builder sh /project/util/local_docker_build/build_gitlab_locally.sh

# Step 8: Build docker images of app.
docker build \
	--build-arg CLIENT_DIRECTORY \
	--build-arg BACKEND_DIRECTORY \
	--build-arg APP_IMAGE_BACKEND_DIRECTORY \
	--build-arg APP_INDEX_HTML_TEMPLATE_DIRECTORY \
	--build-arg DJANGO_SECRET_KEY \
	--build-arg DJANGO_DEBUG \
	--build-arg DJANGO_DATABASE_NAME \
	--build-arg DJANGO_DATABASE_USERNAME \
	--build-arg DJANGO_DATABASE_PASSWORD \
	--build-arg DJANGO_DATABASE_PORT \
	--build-arg DJANGO_DATABASE_HOST \
	--build-arg DJANGO_ALLOWED_HOST_1 \
	--build-arg DJANGO_ALLOWED_HOST_2 \
	--build-arg DJANGO_STATICFILES_RELATIVE_TO_BACKEND_DIRECTORY \
	--build-arg DJANGO_STATIC_ROOT_RELATIVE_TO_BACKEND_DIRECTORY \
	--build-arg DJANGO_MEDIA_ROOT_RELATIVE_TO_BACKEND_DIRECTORY \
	--build-arg DJANGO_STATIC_URL \
	--build-arg DJANGO_MEDIA_URL \
	--build-arg GUNICORN_PORT \
	-t $APP_IMAGE_DEBUG .

docker build \
	--build-arg NGINX_IMAGE_STATICFILES_DESTINATION_DIRECTORY \
	--build-arg NGINX_IMAGE_MEDIAFILES_DESTINATION_DIRECTORY \
	--build-arg CERTBOT_EMAIL \
	--build-arg GUNICORN_PORT \
	--build-arg NGINX_SERVER_NAME \
	-t $NGINX_IMAGE_DEBUG -f nginx/Dockerfile .

docker build
	--build-arg DJANGO_DATABASE_NAME \
	--build-arg DJANGO_DATABASE_USERNAME \
	--build-arg DJANGO_DATABASE_PASSWORD \
	-t $POSTGRES_IMAGE_DEBUG -f postgres/Dockerfile .


# Step 9: Stop the builder container.
docker stop builder


# TODO: make docker-compose for local debug build.
