import RPi.GPIO as GPIO
import time
from playsound import playsound
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

if 'Anti-bark' not in list(r.table_list().run(conn)):
    logging.info("table does not exist, creating...")
    r.table_create("Anti-bark").run(conn)

logging.info("table exists")
conn.close()

#GPIO SETUP
channel = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

def callback(channel):
	if GPIO.input(channel):
		print("Sound Detected!")
	        playsound('highfreq.wav')
                time.sleep(1)
        else:
		print("Sound Detected!")                
	        playsound('highfreq.wav')
                time.sleep(1)

GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(channel, callback)

while True:
	time.sleep(1)
