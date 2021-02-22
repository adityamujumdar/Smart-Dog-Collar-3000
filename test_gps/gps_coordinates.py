from gps import *
import time

import rethinkdb as rdb
import socket
import logging
import sys
import datetime

r = rdb.RethinkDB()

latitude = ' '
longitude = ' '

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M'
    )

HOSTNAME = socket.gethostname()
DB_HOST = "192.168.0.50"
DB_PORT = 28015
DB_NAME = "raspberrypi_p00"

logging.info("Attempting db connection...")
conn = r.connect(DB_HOST, DB_PORT, DB_NAME)
logging.info("Successful DB connection")

logging.info("Checking if db exists")

if DB_NAME not in list(r.db_list().run(conn)):
    logging.info("db does not exist, creating...")
    r.db_create(DB_NAME).run(conn)
logging.info("db exists")

logging.info("Checking to see if table exists")

if 'GPS' not in list(r.table_list().run(conn)):
    logging.info("table does not exists, creating...")
    r.table_create("GPS").run(conn)

logging.info("table exists")
conn.close()

running = True

#latitude = ' '
#longitude = ' '

def getPositionData(gps):
    nx = gpsd.next()
    # For a list of all supported classes and fields refer to:
    # https://gpsd.gitlab.io/gpsd/gpsd_json.html
    if nx['class'] == 'TPV':
        latitude = getattr(nx,'lat', "Unknown")
        longitude = getattr(nx,'lon', "Unknown") 
        print("Your position: lon = " + str(longitude) + ", lat = " + str(latitude))

        if longitude is not None and latitude is not None:
            conn = r.connect(DB_HOST, DB_PORT, DB_NAME)
            timezone = time.strftime("%z")
            reql_tz = r.make_timezone(timezone[:3] + ":" + timezone[3:])

        r.table("GPS").insert(dict(
            lat = str(latitude),
            long = str(longitude),
            datetime=datetime.datetime.now(reql_tz)
            )).run(conn, durability='soft')

        conn.close()
        logging.info("Successful sensor read (Longitude: {:}, Latitude: {:}")

gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE) 

try:
    while running:
        getPositionData(gpsd)
        time.sleep(1.0)

except (KeyboardInterrupt):
    running = False
