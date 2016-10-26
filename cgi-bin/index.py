#!/usr/bin/python3
# -*- coding: UTF-8 -*-

#  Branchement pour le Flash / Distributeur de gouttes
#  http://fritzing.org/projects/optocoupler/

import picamera
import uuid

import RPi.GPIO as GPIO
import time
from multiprocessing import Process
import os
import logging

MJKZZ_PIN = 38  # GPIO 28

LAG = 0.45 	# 0.45s => 330ms
#LAG = 0.5	# 0.5s  => 280ms


def takePicture(imgName):
    try:
        logging.warning("Configure camera ....")
        camera = picamera.PiCamera()
        camera.rotation = 180
        camera.iso = 100
        camera.shutter_speed = 50000 # 0.5s
        camera.capture(imgName)
        logging.warning("Picture taken ....")
    finally:
        camera.close()

def setupGPIO():
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(MJKZZ_PIN, GPIO.OUT)
	GPIO.output(MJKZZ_PIN, GPIO.LOW)

def cleanGPIO():
	GPIO.cleanup()                     # Release resource


imgName = "photos/%s.jpg" % str(uuid.uuid1())
try:
    setupGPIO()
    p = Process(target=takePicture, args=(imgName,))
    p.start()

    logging.warning("Starting MJKZZ ....")
    time.sleep(0.45)
    GPIO.output(MJKZZ_PIN, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(MJKZZ_PIN, GPIO.LOW)
    p.join()
    logging.warning("-- After JOIN --")
   
finally:
    cleanGPIO()
# http://picamera.readthedocs.io/en/release-1.12/recipes2.html#using-a-flash-with-the-camera

html_header = 'Content-type: text/html\r\n\r\n'
 
html_code= '''
<!DOCTYPE html>
<html>
  <head>
     <meta charset="utf-8" />
     <title>DedeDropPi 0.1</title>
  </head>
<body>
<h1>DedeDropPi 0.1</h1>
<img src="../%s"/>
<form>
<input type="submit" value="Nouvel essai"/>
</form>
</body>
</html>
''' % imgName

print(html_header)
print(html_code)

