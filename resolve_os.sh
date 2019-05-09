#!/bin/bash

if [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
	export VBIN="Scripts"
else
	#elif [[ "$OSTYPE" == "linux-gnu" -o "$OSTYPE" == "darwin"* -o "$OSTYPE" == "freebsd"* ]]; then
	# Linux or Mac or FreeBSD
	alias python=python3
	export VBIN="bin"
fi
