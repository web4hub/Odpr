#!/bin/bash
set -eo pipefail

echo "pwd:"
pwd

debian-dind/update_dind_image.sh
if [ ! $? -eq 0 ]; then
	echo "Debian-Dind needed an update so we also update builder..."
	export BUILD=1
fi

builder/update_builder.sh
