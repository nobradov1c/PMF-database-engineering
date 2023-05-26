# PMF-database-engineering
Software engineering for databases, university class

## start the database server

- `docker run --name faks-mysql -e MYSQL_ROOT_PASSWORD=root -p 3306:3306 -d mysql:8.0.33`

## Create the database, tables and generate data

Use mysql workbench to connect to the database server.

Use the following credentials:
user: root
password: root

- run the sql script `create_mysql_schema.sql` to create the database and tables

- run generate-data.py to generate data for the database
