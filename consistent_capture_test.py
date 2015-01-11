#!/usr/bin/env python

folder = "/opt/camera"
ISOs = [100]
speeds = [1000000/8000,1000000/4000,1000000/2000,1000000/1000,1000000/500,
          1000000/250 ,1000000/125, 1000000/60,  1000000/30,  1000000/15,
          1000000/8,   1000000/4,   1000000/2,   1000000,
          #2000000,
          #4000000
         ]

import os
import time
import picamera

with picamera.PiCamera() as camera:
    print(dir(camera))
    camera.resolution = (1024, 768)
    camera.framerate = 30
    camera.hflip = True
    camera.vflip = True 
    # Wait for analog gain to settle on a higher value than 1
    while camera.analog_gain <= 1:
        time.sleep(0.1)
    print(camera.analog_gain)
    print(camera.iso)
    # Now fix the values
    print(camera.exposure_speed)
    print(camera.shutter_speed)
    #camera.shutter_speed = camera.exposure_speed
    camera.exposure_mode = 'off'
    g = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = g
    print(g)
    for ISO in ISOs:
        camera.iso = ISO
        # Finally, take several photos with the fixed settings
        #camera.capture_sequence([folder+'/image%02d.jpg' % i for i in range(10)])
        for speed in speeds:
            camera.shutter_speed = speed
            camera.capture(os.path.join(folder,'image_%s_%s.jpg' % (ISO, str(speed).zfill(7))))
