#!/bin/bash

cd "$(dirname "$0")"

help() {
	echo "Usage: $0 <option>"
	echo "Options:"
	echo "  start:    Start the app setup (if not already running)"
	echo "  stop:     Stop the running app"
	echo "  restart:  Restart the running app"
	echo "  status:   Print status of the app"
	echo "  update:   Perform update of the images (stop, delete old images, update, restart app)"
	echo "  *:        Print this help text"
}

echo DOCKER_PW | docker login -u DOCKER_USER --password-stdin DOCKER_REGISTRY 2>/dev/null

running_containers() {
	echo $(docker-compose ps | grep -c "APP_NAME.*Up")
}

status_compose() {
	docker-compose ps
	docker-compose top
}

start_containers() {
	docker-compose up -d
}

stop_compose() {
	docker-compose stop
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

update_images() {
	stop_compose
	docker image prune --force
	docker image rm -f $(docker images | grep "^<none>" | awk '{ print $3 }')
	docker-compose pull
	start_compose
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
		"$0" stop
		"$0" start
		;;
	status)
		echo "Status:"
		status_compose
		;;
	update)
		echo "Update:"
		update_images
		;;
	*)
		help
		exit 1
esac

