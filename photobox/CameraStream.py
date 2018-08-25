import sys
import os
import time
import RPi.GPIO as GPIO
import signal
import pygame
import pygame.camera
from pygame.locals import *
from threading import Thread
import picamera
import io
from PIL import Image

DEVICE = '/dev/video0'
SIZE = (800, 480)
SIZE2 = (1920, 1080)
WHITE = 255, 255, 255
BUTTON_PIN=20
MODE=""   #GLOBAL
MSG=""    #GLOBAL

photoPath = "/home/pi/Documents/photobox/images/"
#pathFilename=photoPath+photoName


def signal_handler(signal, frame):
        print('Fermeture via CTRL+C')
        sys.exit(0)
 
signal.signal(signal.SIGINT, signal_handler)


class Retardateur(Thread):
    
    def __init__(self, name,modeSuivant):
        Thread.__init__(self)
        self.name = name
        self.mode=modeSuivant
        print("Initialisation du Thread "+name)

    def run(self):
        print(time.strftime("%H:%M:%S"))
        global MODE
        global MSG
        MSG="3"
        print("3")
        print(time.strftime("%H:%M:%S"))
        time.sleep(1)
        MSG="2"
        print("2")
        print(time.strftime("%H:%M:%S"))
        time.sleep(1)
        MSG="1"
        print("1")
        print(time.strftime("%H:%M:%S"))
        time.sleep(1)
        MODE=self.mode
        MSG=""
        print(self.mode)
        time.sleep(1)
        print(time.strftime("%H:%M:%S"))

def camstream():
    global MODE
    global MSG
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, bouncetime=1000)

    pygame.init()
    pygame.camera.init()
    pygame.mouse.set_visible(False)
    horloge = pygame.time.Clock()
    myfont = pygame.font.Font(None, 30)
    display = pygame.display.set_mode(SIZE, FULLSCREEN)
    #display = pygame.display.set_mode(SIZE,0)
    
    font=pygame.font.SysFont('freesans', (180))
    font2=pygame.font.SysFont('freesans', (30))
    camera = pygame.camera.Camera(DEVICE, SIZE)
    camera.start()
    camera.set_controls(hflip = False, vflip = True,brightness=50)
    print(camera.get_controls())
    screen = pygame.surface.Surface(SIZE, 0, display)
    screen2 = pygame.surface.Surface(SIZE2, 0, display)

    capture = True

    while capture:
        
        #GESTION des events:
        for event in pygame.event.get():
            if event.type == QUIT:
                print('Fermeture via ALT+F4')
                capture = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: 
                    print('Fermeture via ECHAP')
                    capture = False
        if  GPIO.event_detected(BUTTON_PIN):
            if MODE=="":
               MODE="TEMPO"
               print("======== BOUTON PRESSED ========")
               thread_1 = Retardateur("Tempo photo","photo")
               thread_1.start()
            else:
                print("======== BOUTON ALREADY PRESSED ========")

        #GESTION des actions:
        if MODE =="photo":
            print("Take picture!")
            MODE="load"
            #pygame.image.save(screen,"thumb.jpg")
            screen = camera.get_image(screen)
            camera.stop()
            photoName = time.strftime("%Y%m%d%H%M%S") + "_photobooth.jpg"
            os.system("raspistill -n -w 3280 -h 2464 -vf -q 100 -t 1 -o " + photoPath + photoName)
            camera.start()
            print(time.strftime("%H:%M:%S"))
            cmd="scp -B "+photoPath + photoName+" pi@192.168.0.22:/home/pi/Documents/Visionneuse/images/"
            os.system(cmd)
            print(time.strftime("%H%M%S"))
        elif MODE=="load":
            print("Display picture")
            MODE="display"
            thread_2 = Retardateur("Tempo display","") 
            thread_2.start()
        elif MODE=="display":
            postionText=(760,410)
            mytext = font2.render(MSG, True, WHITE)
            time.sleep(0.5)
        else:
            #Streaming camera:            
            screen = camera.get_image(screen)
            postionText=(360,140)
            mytext = font.render(MSG, True, WHITE)

        #refresh
        display.blit(screen, (0,0))
        #Surcharge image
        display.blit(mytext, postionText)
        pygame.display.update()

    camera.stop()
    pygame.quit()
    return

if __name__ == '__main__':
    camstream()
