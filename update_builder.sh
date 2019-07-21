#!/bin/bash
set -eo pipefail

# Return 0 if builder image on registry is up to date. return 1 if needs to be updated.
compare_images() {
	builder_nodes_sum=$(docker run --entrypoint node_modules_checksum.sh "${BUILDER_IMAGE}")
	repo_nodes_sum=$(sha256sum client/package.json)
	if [ "${builder_nodes_sum}" != "${repo_nodes_sum}" ]; then
		return 1;
	else
		builder_pip_sum=$(docker run --entrypoint pip_requirements_checksum.sh "${BUILDER_IMAGE}")
		repo_pip_sum=$(sha256sum backend/requirements.txt)
		if [ "${builder_pip_sum}" != "${repo_pip_sum}" ]; then
			return 1;
		else
			return 0;
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
	compare_images
	if [ $? -eq 1 ]; then
		echo "Builder out of date, updating image..."
		BUILD=1
	else
		echo "Builder up to date, nothing to do in this stage."
	fi
fi

if [ 0$BUILD -eq 1 ]; then
	docker build -t "${BUILDER_IMAGE}" -f builder/Dockerfile .
	docker push "${BUILDER_IMAGE}"
fi
