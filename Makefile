PASSWORD = change-me-123
USER = sa
CONTAINER = mssql
SQLCMD = podman exec -it ${CONTAINER} /opt/mssql-tools18/bin/sqlcmd -U ${USER} -P ${PASSWORD} -C 
RUNSQL = podman exec ${CONTAINER} /opt/mssql-tools18/bin/sqlcmd -U ${USER} -P ${PASSWORD} -C -i
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

