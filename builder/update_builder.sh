#!/bin/bash
set -eo pipefail

# Return 0 if builder image on registry is up to date. return 1 if needs to be updated.
compare_images() {
	builder_nodes_sum=$(docker run --entrypoint "${BUILDER_VERSION_SCRIPTS_DIRECTORY}/node_modules_checksum.sh" "${BUILDER_IMAGE}")
	repo_nodes_sum=$(sha256sum client/package.json | awk '{printf $1}') # client stays hardcoded as here the host client is focused.
	echo "Builder's checksum for package.json was: $builder_nodes_sum"
	echo "Repo's checksum for package.json was:    $repo_nodes_sum"
	set +e
	if [ "${builder_nodes_sum}" != "${repo_nodes_sum}" ]; then
		echo "Checksums did not match."
		return 1;
	else
		set -e
		builder_pip_sum=$(docker run --entrypoint "${BUILDER_VERSION_SCRIPTS_DIRECTORY}/pip_requirements_checksum.sh" "${BUILDER_IMAGE}")
		repo_pip_sum=$(sha256sum backend/requirements.txt | awk '{printf $1}') # backend stays hardcoded as here the host backend is focused.
		echo "Builder's checksum for requirements.txt was: $builder_pip_sum"
		echo "Repo's checksum for requirements.txt was:    $repo_pip_sum"
		set +e
		if [ "${builder_pip_sum}" != "${repo_pip_sum}" ]; then
			echo "Checksums did not match."
			return 1;
		else
			set -e
			builder_dockerfile_sum=$(docker run --entrypoint "${BUILDER_VERSION_SCRIPTS_DIRECTORY}/dockerfile_checksum.sh" "${BUILDER_IMAGE}")
			repo_dockerfile_sum=$(sha256sum builder/Dockerfile | awk '{printf $1}') # builder stays hardcoded as here the host builder is focused.
			echo "Builder's checksum for its Dockerfile was: $builder_dockerfile_sum"
			echo "Repo's checksum for its Dockerfile was:    $repo_dockerfile_sum"
			set +e
			if [ "${builder_dockerfile_sum}" != "${repo_dockerfile_sum}" ]; then
				echo "Checksums did not match."
				return 1;
			else
				echo "Checksums did match."
				return 0;
			fi
		fi
	fi
}

set +e
docker pull "${BUILDER_IMAGE}" 2>/dev/null
if [ ! $? -eq 0 ]; then
	NOT_FOUND=1
fi
set -e

if [ 0$NOT_FOUND -eq 1 ]; then
	echo "No docker image found in registry, building from scratch..."
	BUILD=1
else
	set +e
	compare_images
	result=$?
	set -e
	if [ $result -eq 1 ]; then
		echo "Builder out of date, updating image..."
		BUILD=1
	else
		echo "Builder up to date, nothing to do in this stage."
	fi
fi

if [ 0$BUILD -eq 1 ]; then
	docker build \
		--build-arg REPO_COPY_DIRECTORY \
		--build-arg CLIENT_DIRECTORY \
		--build-arg BACKEND_DIRECTORY \
		--build-arg BUILDER_VERSION_SCRIPTS_SRC_DIRECTORY \
		--build-arg BUILDER_VERSION_SCRIPTS_DIRECTORY \
		--build-arg BUILDER_VENV_DIRECTORY \
		--build-arg BUILDER_NODE_MODULES_SRC_DIRECTORY \
		-t "${BUILDER_IMAGE}" \
		-f builder/Dockerfile .
	docker push "${BUILDER_IMAGE}"
fi
