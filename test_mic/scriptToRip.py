import time
import math
import smbus
import rethinkdb as rdb
import socket
import datetime
import logging
import sys



r = rdb.RethinkDB()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M')


HOSTNAME = socket.gethostname()
DB_HOST = "192.168.0.20"
DB_PORT = 28015
DB_NAME = "raspberrypi_gc3"

logging.info("Attempting db connection...")
conn = r.connect(DB_HOST, DB_PORT, DB_NAME)
logging.info("Successful DB connection")

logging.info("Checking if db exists")

if DB_NAME not in list(r.db_list().run(conn)):
    logging.info("db does not exist, creating...")
    r.db_create(DB_NAME).run(conn)
    logging.info("db exists")

logging.info("Checking to see if table exists")

if 'Anti-bark' not in list(r.table_list().run(conn)):
    logging.info("table does not exist, creating...")
    r.table_create("Anti-bark").run(conn)

logging.info("table exists")

conn.close()

r.connect(DB_HOST,DB_PORT).repl()
cursor = r.db(DB_NAME).table('Anti-bark').run()

for database in cursor:
    string = str(database)
    string = string[56:]
    string = string[:1]
    print(string)










