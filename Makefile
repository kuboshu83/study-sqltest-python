PASSWORD = change-me
USER = sa
CONTAINER = test-db
DBNAME = postgres
SQLCMD = podman exec -it ${CONTAINER} psql -h localhost -p 5432 -U ${USER} -d ${DBNAME}
RUNSQL = podman exec ${CONTAINER} psql -h localhost -p 5432 -U ${USER} -d ${DBNAME} -f
CP = podman cp

.PHONY: start
start:
	@podman compose up -d

.PHONY: stop
stop:
	@podman compose down

.PHONY: restart
restart: stop-db start-db

.PHONY: connect-db
connect:
	@${SQLCMD}

.PHONY: arrange
arrange:
	@${CP} ./test/data.sql ${CONTAINER}:/tmp/data.sql
	@${CP} ./target.sql ${CONTAINER}:/tmp/target.sql
	@${RUNSQL} /tmp/data.sql
	@${RUNSQL} /tmp/target.sql

