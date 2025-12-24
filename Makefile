USER = sa
CONTAINER = test-db
DBNAME = postgres
SQLCMD = podman exec -it ${CONTAINER} psql -h localhost -p 5432 -U ${USER} -d ${DBNAME}

.PHONY: start
start:
	@podman compose up -d

.PHONY: stop
stop:
	@podman compose down

.PHONY: restart
restart: stop start

.PHONY: connect
connect:
	@${SQLCMD}