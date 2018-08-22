import random
import sys
import os
import os.path
import glob
import pygame
import time
from pygame.locals import *
from threading import Thread
import pyinotify

print("************************");
print("*   Visionneuse Image  *");
print("************************");

CHANGEPICTURE = USEREVENT+1
TEMPO=10
BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREEN = 0, 255, 0
YELLOW = 255,242,0

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        print ("///////////Creating:", event.pathname)
        thread_1.my_list.append(getImageName(event.pathname))

class Visionneuse(Thread):
	def __init__(self, name):
		Thread.__init__(self)
		self.name = name
		self.arret=0
		print("Initialisation du Thread "+name)
		self.path=os.getcwd()
		self.path=self.path+"/Documents/Visionneuse/images/"
		print(self.path)
		self.my_list = listdirectory(self.path)
		self.maxItem=len(self.my_list)-1
		self.index=-1

	def run(self):
		while self.arret==0:
			if( self.index == self.maxItem):
				#self.my_list=listdirectory(self.path)
				maxItemnew=len(self.my_list)-1 #Verification si nouvelles images disponibles
				if(self.maxItem == maxItemnew):
					self.index=0
				else:
					self.maxItem=maxItemnew
					self.index=self.index+1
			else:
				self.index=self.index+1
			StringForDisplay= ""+str(self.index+1)+" / "+str(self.maxItem+1)
			my_event = pygame.event.Event(CHANGEPICTURE, message="/home/pi/Documents/Visionneuse/images/"+getImageName(self.my_list[self.index]),text=StringForDisplay)
			pygame.event.post(my_event)
			time.sleep(TEMPO)
			
	def stop(self):
		print("Arret du Thread")
		self.arret=1

# Lib TOOLS:
def listdirectory(path):  
	fichier=[]  
	l = glob.glob(path+'/*')
	l.sort(key=os.path.getmtime)
	for i in l:  
		if os.path.isdir(i): fichier.extend(listdirectory(i))  
		else: fichier.append(i)  
	return fichier

def getImageName(path):
	a=os.path.split(path)
	return a[1]


#Initialisation de la bibliotheque Pygame
pygame.init()
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
surface = pygame.display.Info()
print("Surface information:")
print(surface)
fenetre = pygame.display.set_mode((surface.current_w, surface.current_h), pygame.FULLSCREEN)
#fenetre = pygame.display.set_mode((surface.current_w, surface.current_h), RESIZABLE)
font=pygame.font.SysFont('freesans', 18)

# Inotify: 
wm = pyinotify.WatchManager()  # Watch Manager
mask = pyinotify.IN_CREATE # watched events

notifier = pyinotify.ThreadedNotifier(wm, EventHandler())
notifier.start()
wdd = wm.add_watch('/home/pi/Documents/Visionneuse/images/', mask, rec=True)

thread_1 = Visionneuse("Myvisionneuse")
thread_1.start()

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			notifier.stop()
			thread_1.stop()
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				print('Fermeture via ECHAP')
				notifier.stop()
				thread_1.stop()
				pygame.quit()
				sys.exit()
		if event.type == CHANGEPICTURE:
			print("Change picture:"+time.strftime("%H%M%S"))
			print(event.message)
			print(event.text)
			try:
				imageToLoad=event.message
				fond = pygame.image.load(imageToLoad)
				fond = pygame.transform.scale(fond, (surface.current_w, surface.current_h))
				fenetre.blit(fond, (0,0))
			except Exception:
				print("Probleme load image:"+imageToLoad)
			
			#fondBas=pygame.Surface((surface.current_w,100))
			#fondBas.fill(WHITE)
			#fenetre.blit(fondBas, (0,surface.current_h-100))
			
			fondBas = pygame.image.load("/home/pi/Documents/Visionneuse/Skyline1C.png")
			fondBas_width=fondBas.get_width()*1
			fondBas_height=fondBas.get_height()*1
			
			fondBas = pygame.transform.scale(fondBas, (fondBas_width,fondBas_height))
			fenetre.blit(fondBas, (200,surface.current_h-fondBas_height))
			mytext = font.render(event.text, True, WHITE)  # True pour antialiasing
			fenetre.blit(mytext, (surface.current_w-75,surface.current_h-20))
			pygame.display.flip()
			pygame.time.wait(250)
os.system("pause")