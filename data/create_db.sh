rm database.db
sqlite3 database.db < schemas.sql
sqlite3 database.db < inserts.sql
