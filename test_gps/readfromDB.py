from gps import *
import time

import rethinkdb as rdb
import socket
import logging
import sys
import datetime

r = rdb.RethinkDB()
r.connect("192.168.0.50", 28015, "raspberrypi_p00").repl()
cursor = r.table("GPS").pluck("lat", "long").run()
for document in cursor:
  print(document)
