PASSWORD = change-me
USER = sa
CONTAINER = test-db
DBNAME = postgres
SQLCMD = podman exec -it ${CONTAINER} psql -h localhost -p 5432 -U ${USER} -d ${DBNAME}
RUNSQL = podman exec ${CONTAINER} psql -h localhost -p 5432 -U ${USER} -d ${DBNAME} -f
CP = podman cp
TARGET = "_"

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

.PHONY: arrange
arrange:
	@${CP} ./queries/${TARGET}/test/data.sql ${CONTAINER}:/tmp/data.sql
	@${CP} ./queries/${TARGET}/target.sql ${CONTAINER}:/tmp/target.sql
	@${RUNSQL} /tmp/data.sql
	@${RUNSQL} /tmp/target.sql

.PHONY: test
test:
	@python3 ./queries/${TARGET}/run-test.py
