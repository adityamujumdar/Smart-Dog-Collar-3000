import RPi.GPIO as GPIO
import time
import math
import smbus
import rethinkdb as rdb
import socket
import datetime
import logging
import sys
import pygame
import mixer
from pygame import mixer

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

pygame.mixer.init()
pygame.mixer.music.load("highfreq.wav")

#GPIO SETUP
channel = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

def callback(channel):
    if GPIO.input(channel):
        print("Sound Detected!")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
        time.sleep(1)
    else:	 
        print("Sound Detected!") 
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue 
        time.sleep(1)


GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(channel, callback)


if channel is not None:
    conn = r.connect(DB_HOST, DB_PORT, DB_NAME)
    
    r.table("Anti-bark").insert(dict(signal = 1)).run(conn, durability ='soft')
    conn.close()

while True:
	time.sleep(1)
