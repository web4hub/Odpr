#!/bin/bash

if [ "$OSTYPE" = "cygwin" -o "$OSTYPE" = "msys" -o "$OSTYPE" = "win32" ]; then
	export VBIN="Scripts"
	export PYTHON="python"
else
	#elif [[ "$OSTYPE" == "linux-gnu" -o "$OSTYPE" == "darwin"* -o "$OSTYPE" == "freebsd"* ]]; then
	# Linux or Mac or FreeBSD
	export VBIN="bin"
	export PYTHON="python3"
fi
