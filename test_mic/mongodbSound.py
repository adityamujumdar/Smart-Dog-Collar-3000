import RPi.GPIO as GPIO
import time
import math
import smbus
from pymongo import MongoClient
import socket
import datetime
import logging
import sys
import pygame


mongo = MongoClient("mongodb+srv://epascua2:dCfGAzeEwD9PhHFF@autodoggo.pxxuh.mongodb.net/BarkFlag?retryWrites=true&w=majority")
db = mongo.BarkFlag
triggers = db.triggers


pygame.mixer.init()
pygame.mixer.music.load("highfreq.wav")

##GPIO SETUP
channel = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

flag = {'anti-bark': 'ON'}
signal = 0 

def callback(channel):

    if GPIO.input(channel): 
        signal = 1
        flag = {'anti-bark': 'ON'}
        result = triggers.insert_one(flag)
        print("Sound Detected!")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
        time.sleep(1)
        
    else:
        time.sleep(1)



GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=500)

GPIO.add_event_callback(channel, callback)

while True:

    
    flag = {'anti-bark': 'OFF'}
    result = triggers.insert_one(flag)
    time.sleep(5)







