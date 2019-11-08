#!/usr/bin/env python3
'''
Created on 7 nov. 2019

@author: lpgeneau
'''

from datetime import datetime
import RPi.GPIO as GPIO  # @UnresolvedImport
from time import sleep
import requests
import json

server_begin_url = "http://192.168.1.16:8888/"
server_end_url = "motion_sensor"

PIN_SENSOR = 21

def stateChanged(channel):
    print('state changed')
    isDetected = GPIO.input(PIN_SENSOR)
    
    data = { 'motion detected': isDetected, 'date': datetime.today().__str__() }
    
    r = requests.post(server_begin_url+server_end_url, data=json.dumps(data))  # @UnusedVariable
    print("post request send")
    #print(r.status_code)
    
if __name__ == '__main__':
    
    # set up BCM GPIO numbering
    GPIO.setmode(GPIO.BCM)     
    GPIO.setwarnings(False)
    
    # Set up motion sensor connected pin as an input pin
    GPIO.setup(PIN_SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    print('sensor set')
    
    GPIO.add_event_detect(PIN_SENSOR, GPIO.BOTH, callback=stateChanged, bouncetime=300) 

    try:
        while True:
            sleep(1)
            
    except KeyboardInterrupt:
        GPIO.cleanup()         # clean up
        print("All cleaned up.")