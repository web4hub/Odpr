#!/bin/bash

cd "$(dirname "$0")"

help() {
	echo "Usage: $0 <option>"
	echo "Options:"
	echo "  start:    Start the nginx-proxy setup (if not already running)"
	echo "  stop:     Stop a running nginx-proxy"
	echo "  restart:  Restart a running nginx-proxy"
	echo "  status:   Print status of the nginx-proxy"
	echo "  *:        Print this help text"
}

running_containers() {
	echo $(docker-compose -f config/docker-compose.yml ps | grep -c "nginx-proxy.*Up")
}

status_compose() {
	docker-compose -f config/docker-compose.yml ps
	docker-compose -f config/docker-compose.yml top
}

start_containers() {
	docker network create nginx-proxy 2>/dev/null
	docker-compose -f config/docker-compose.yml up -d
}

stop_compose() {
	docker-compose -f config/docker-compose.yml stop
}

start_compose() {
	if [ $(running_containers) -eq 0 ]; then
		start_containers
	elif [ ! $(running_containers) -eq 3 ]; then
		echo "Error: Some containers are up, but not all of them. Attempting complete restart..."
		stop_compose
		start_containers
	else
		echo "Containers already up and running."
	fi
}


case "$1" in
	start)
		echo "Start"
		start_compose
		;;
	stop)
		echo "Stop"
		stop_compose
		;;
	restart|reload)
		echo "Restart"
		stop_compose
		start_compose
		;;
	status)
		echo "Status:"
		status_compose
		;;
	*)
		help
		exit 1
esac

