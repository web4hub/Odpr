#!/bin/bash
set -eo pipefail

# $1 env to be inserted into file
# $2 relative or total path to file

help() {
	echo "$0"
	echo "Usage: $0 [ENV] [PATH_TO_FILE] <options>"
	echo ""
	echo "Options:"
	echo "  --help          Print this help text"
	echo "  ENV       			An existing environment variable which is contained in the target file with the same name, whose value will be injected there."
	echo "  PATH_TO_FILE   	A relative or absolute path to the file where the value should be injected"
	echo "  --test          cat the output to the commandline instead of writing the changes to the file"
	echo "  --force         Also allow empty variable to be inserted."
	echo ""
	echo "Example: $0 INJECT_SERVER_NAME ./inject_script_test_file --test"
}

if [ "$1" == "--help" ]; then
	help
	exit 0;
fi

if [ "$1" == "" -o "$2" == "" ]; then
	help
	exit 1;
fi

ENV="${1}"
VALUE="${!ENV}"
FILE="${2}"

if [ -z "${VALUE}" ] && [ "$3" != "--force" ] && [ "$4" != "--force" ]; then
	echo "ERROR: Env is empty: ${ENV}" >&2
	exit 1
fi

if [ "$3" == "--test" ]; then
	cat "${FILE}" | sed "s~${ENV}~${VALUE}~g"
else
	sed -i "s~${ENV}~${VALUE}~g" ${FILE}
fi
