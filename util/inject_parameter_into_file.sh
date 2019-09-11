#!/bin/bash
set -eo pipefail

# $1 key to be replaced by value
# $2 value to inject to location of KEY
# $3 relative or total path to file

help() {
	echo "$0"
	echo "Usage: $0 [KEY] [VALUE] [PATH_TO_FILE] <options>"
	echo ""
	echo "Options:"
	echo "  --help          Print this help text"
	echo "  KEY       			A string which is contained one or more times in the given file, to be replaced by the given value"
	echo "  VALUE     			The value which should be injected into the file"
	echo "  PATH_TO_FILE   	A relative or absolute path to the file where the value should be injected"
	echo "  --test          cat the output to the commandline instead of writing the changes to the file"
	echo ""
	echo "Example: $0 INJECT_SERVER_NAME example.com ./inject_script_test_file --test"
}

if [ "$1" == "--help" ]; then
	help
	exit 0;
fi

if [ "$1" == "" -o "$2" == "" -o "$3" == "" ]; then
	help
	exit 1;
fi

if [ "$4" == "--test" ]; then
	cat "$3" | sed "s~${1}~${2}~g"
else
	sed -i "s~${1}~${2}~g" ${3}
fi
