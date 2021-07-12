m1=gateway
m2=gestione_utenti
m3=gestione_prenotazioni
dc=docker-compose.yml


logs:
	echo "I'm going to show you container's logs"
	docker-compose -f "$(m1)/$(dc)" logs
	docker-compose -f "$(m2)/$(dc)" logs
	docker-compose -f "$(m3)/$(dc)" logs
	
build:
	echo "Building all containers"
	docker-compose -f "$(m1)/$(dc)" build
	docker-compose -f "$(m2)/$(dc)" build
	docker-compose -f "$(m3)/$(dc)" build

up:
	echo "Bringing containers up"
	docker-compose -f "$(m1)/$(dc)" up -d
	docker-compose -f "$(m2)/$(dc)" up -d
	docker-compose -f "$(m3)/$(dc)" up -d
	
down:
	echo "Putting containers down"
	docker-compose -f "$(m1)/$(dc)" down
	docker-compose -f "$(m2)/$(dc)" down
	docker-compose -f "$(m3)/$(dc)" down
	
start:
	echo "Starting already built containers"
	docker-compose -f "$(m1)/$(dc)" start
	docker-compose -f "$(m2)/$(dc)" start
	docker-compose -f "$(m3)/$(dc)" start

stop:
	echo "Stopping containers, without erasing data"
	docker-compose -f "$(m1)/$(dc)" stop
	docker-compose -f "$(m2)/$(dc)" stop
	docker-compose -f "$(m3)/$(dc)" stop
