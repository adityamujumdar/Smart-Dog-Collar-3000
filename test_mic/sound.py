import RPi.GPIO as GPIO
import time
from playsound import playsound


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
