#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import pygame


#GPIO SETUP
channel = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

#load wav file

pygame.mixer.init()
pygame.mixer.music.load("highfreq.wav")

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

while True:
    time.sleep(1)
