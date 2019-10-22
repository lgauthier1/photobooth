import os
import time

while True:
    if(os.system('ls /media/pi/LGA') == 0):
        os.system('cp -R ~/Documents/Visionneuse/images /media/pi/LGA/')
    else:
        print('no copy...')
    time.sleep(300)
