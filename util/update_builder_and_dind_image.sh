#!/bin/bash
set -eo pipefail

result=$(sh debian-dind/update_dind_image.sh)
if [ ${result} == "UPDATED" ]; then
	echo "Debian-Dind needed an update so we also update builder..."
	export BUILD=1
fi

sh builder/update_builder.sh
