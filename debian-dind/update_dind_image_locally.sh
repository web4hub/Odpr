#!/bin/bash
set -eo pipefail

# Return 0 if builder image on registry is up to date. return 1 if needs to be updated.
compare_images() {
	dind_sum=$(docker run --entrypoint "${DIND_VERSION_SCRIPTS_DIRECTORY}/image_checksum.sh" "${DIND_IMAGE}")
	SUM_1=$(sha256sum "${DIND_VERSION_SCRIPTS_SRC_DIRECTORY}/Dockerfile" | awk '{printf $1}')
	SUM_2=$(sha256sum "${DIND_VERSION_SCRIPTS_SRC_DIRECTORY}/dind_script.sh" | awk '{printf $1}')
	SUM_3=$(sha256sum "${DIND_VERSION_SCRIPTS_SRC_DIRECTORY}/entrypoint.sh" | awk '{printf $1}')
	repo_sum="${SUM_1}${SUM_2}${SUM_3}"
	echo "Dind's checksum for whole image was:    $dind_sum"
	echo "Repo's checksum for whole image was:    $repo_sum"
	set +e
	if [ "${dind_sum}" != "${repo_sum}" ]; then
		echo "Checksums did not match."
		return 1;
	else
		echo "Checksums did match."
		return 0;
	fi
}

cd /project
source util/local_docker_build/variables.sh

set +e
if [[ "$(docker images -q ${DIND_IMAGE} 2> /dev/null)" == "" ]]; then
	NOT_FOUND=1
fi
set -e

if [ 0$NOT_FOUND -eq 1 ]; then
	echo "No docker image found locally, building from scratch..."
	export BUILD=1
else
	set +e
	compare_images
	result=$?
	set -e
	if [ $result -eq 1 ]; then
		echo "Custom debian-dind out of date, updating image..."
		export BUILD=1
	else
		echo "Custom debian-dind up to date, nothing to do..."
	fi
fi

if [ 0$BUILD -eq 1 ]; then
	docker build \
		--build-arg DIND_VERSION_SCRIPTS_SRC_DIRECTORY \
		--build-arg DIND_VERSION_SCRIPTS_DIRECTORY \
		-t "${DIND_IMAGE}" \
		-f "${DIND_VERSION_SCRIPTS_SRC_DIRECTORY}"/Dockerfile .
fi
