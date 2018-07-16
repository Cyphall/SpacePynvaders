import pygame
import logging
import time
import os

#=== <Classes> ===#
class display():
	def __init__(self, size=(640, 480)):
		self.display = pygame.display.set_mode(size)
		pygame.display.set_caption("Space Pynvaders")
		self.aliens = []
		self.shot = None
		self.player = None
		self.sounds = soundInit()
	
	
	def initAliens(self):
		for y in range(5):
			for x in range(11):
				if (y == 0 or y == 1):
					temp = alien("sprites/10")
					temp.setPos(x=x*60, y=250-y*60)
					self.aliens.append(temp)
				elif (y == 2 or y == 3):
					temp = alien("sprites/20")
					temp.setPos(x=x*60, y=250-y*60)
					self.aliens.append(temp)
				elif (y == 4):
					temp = alien("sprites/30")
					temp.setPos(x=x*60, y=250-y*60)
					self.aliens.append(temp)
	
	
	def playMusic(self, music):
		self.sounds[music].play()
	
	
	def hit(self, alien):
		alien.actual = 2
		self.sounds["boom"].play()
		self.shot = None
	
	
	def delAlien(self, alien):
		self.aliens.remove(alien)
	
	def initPlayer(self, path):
		self.player = player(path)
	
	
	def miss(self):
		self.shot = None
	
	
	def fire(self):
		if (self.shot is None):
			self.sounds["shoot"].play()
			self.shot = shot("sprites/shot.png", (self.player.getPos()["x"]+24, self.player.getPos()["y"]-12))
	
	
	def render(self):
		self.display.fill((pygame.Color("black")))
		for s in self.aliens:
			s.render(self.display)
		if (self.player is not None):
			self.player.render(self.display)
		if (self.shot is not None):
			self.shot.render(self.display)
		pygame.display.flip()
	
	
	def getAliens(self, copy=False):
		if (copy):
			return self.aliens[:]
		return self.aliens
	
	
	def getPlayer(self):
		return self.player
	
	
	def getShot(self):
		return self.shot
	
	
	def shotExists(self):
		if (self.shot is not None):
			return True
		return False
	
	
	def getDisplaySize(self):
		return {"x":pygame.display.Info().current_w, "y":pygame.display.Info().current_h} 


class sprite(object):
	def __init__(self, path, pos=(0, 0)):
		try:
			self.sprite = pygame.image.load(path).convert_alpha()
			self.pos = {"x":pos[0], "y":pos[1]}
			self.size = {"x":self.sprite.get_size()[0], "y":self.sprite.get_size()[1]}
			logging.info("Sprite successfully loaded from "+path)
		except Exception as e:
			logging.error(e)
	
	
	def setPos(self, x=None, y=None):
		if (x is not None):
			self.pos["x"] = x
		if (y is not None):
			self.pos["y"] = y
		
	
	
	def getPos(self):
		return self.pos
	
	
	def getSize(self):
		return self.size
	
	
	def render(self, display):
		display.blit(self.sprite, (self.pos["x"], self.pos["y"]))
	

class alien(sprite):
	def __init__(self, path, pos=(0, 0)):
		try:
			self.sprite = [pygame.image.load(path+"_0.png").convert_alpha(), pygame.image.load(path+"_1.png").convert_alpha(), pygame.image.load("sprites/boom.png").convert_alpha()]
			self.actual = 0
			self.pos = {"x":pos[0], "y":pos[1]}
			self.size = {"x":self.sprite[0].get_size()[0], "y":self.sprite[0].get_size()[1]}
			logging.info("Sprite successfully loaded from "+path)
		except Exception as e:
			logging.error(e)
	
	
	def move(self, dir, display):
		if (self.actual == 1):
			self.actual = 0
		else:
			self.actual = 1
		if (dir == "l"):
			self.pos["x"] -= 8
			if (self.pos["x"] <= 0):
				return True
		elif (dir == "r"):
			self.pos["x"] += 8
			if (self.pos["x"]+self.size["x"] >= display.getDisplaySize()["x"]):
				return True
		elif (dir == "d"):
			self.pos["y"] += 40
		return False
	
	
	def render(self, display):
		display.blit(self.sprite[self.actual], (self.pos["x"], self.pos["y"]))


class player(sprite):
	def move(self, dir, display):
		if (dir == "l"):
			self.pos["x"] -= 4
			if (self.pos["x"] < 0):
				self.pos["x"] = 0
		elif (dir == "r"):
			self.pos["x"] += 4
			if (self.pos["x"]+self.size["x"] > display.getDisplaySize()["x"]):
				self.pos["x"] = display.getDisplaySize()["x"]-self.size["x"]


class shot(sprite):
	def move(self):
		self.pos["y"] -= 16
#=== </Classes> ===#


#=== <Fonctions> ===#
def collision(a, b):
	if (a.getPos()["x"] >= b.getPos()["x"]+b.getSize()["x"]):
		return False
	if (a.getPos()["x"]+a.getSize()["x"] <= b.getPos()["x"]):
		return False
	if (a.getPos()["y"] >= b.getPos()["y"]+b.getSize()["y"]):
		return False
	if (a.getPos()["y"]+a.getSize()["y"] <= b.getPos()["y"]):
		return False
	return True

def soundInit():
	sounds = {}
	for file in os.listdir("sounds"):
		sounds[os.path.splitext(file)[0]] = pygame.mixer.Sound("sounds/"+file)
		sounds[os.path.splitext(file)[0]].set_volume(0.05)
	return sounds
#=== </Fonctions> ===#


#=== <Main> ===#
def main():
	logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
	pygame.mixer.pre_init(44100, -16, 1, 512)
	pygame.init()
	size = (712, 740)
	d = display(size=size)
	d.initAliens()
	d.initPlayer("sprites/player.png")
	d.getPlayer().setPos(y=size[1]-(d.getPlayer().getSize()["y"]))
	d.render()
	fps = 60
	
	running = True
	
	dir = "r"
	nextDir = None
	turning = False
	
	toDelete = None
	explosion = False
	
	music = 1
	timing = 0
	
	while (running):
		for alien in d.getAliens(copy=True):
			for event in pygame.event.get():
				if (event.type == pygame.QUIT):
					running = False
			if (pygame.key.get_pressed()[97] == True or pygame.key.get_pressed()[276] == True):
				d.getPlayer().move("l", d)
			if (pygame.key.get_pressed()[100] == True or pygame.key.get_pressed()[275] == True):
				d.getPlayer().move("r", d)
			
			
			if (alien.move(dir, d) and turning == False):
				turning = True
			
			if (explosion):
				for i in range(20):
					timing += 1
					if (timing >= round(len(d.getAliens())/1.5)+5):
						timing = 0
						d.playMusic("music"+str(music))
						music += 1
						if (music == 5):
							music = 1
					for event in pygame.event.get():
						if (event.type == pygame.QUIT):
							running = False
					if (pygame.key.get_pressed()[97] == True or pygame.key.get_pressed()[276] == True):
						d.getPlayer().move("l", d)
					if (pygame.key.get_pressed()[100] == True or pygame.key.get_pressed()[275] == True):
						d.getPlayer().move("r", d)
					d.render()
					time.sleep(1/fps)
				explosion = False
				d.delAlien(toDelete)
				toDelete = None
			
			timing += 1
			if (timing >= round(len(d.getAliens())/1.5)+5):
				timing = 0
				d.playMusic("music"+str(music))
				music += 1
				if (music == 5):
					music = 1
			
			if (pygame.key.get_pressed()[32] == True):
				d.fire()
			
			if (d.shotExists()):
				d.getShot().move()
				if (d.getShot().getPos()["y"] < 0):
					d.miss()
				else:
					for al in d.getAliens():
						if (collision(d.getShot(), al)):
							d.hit(al)
							toDelete = al
							explosion = True
							break
			
			
			
			
			d.render()
			time.sleep(1/fps)
		
		
		if (len(d.getAliens()) == 0):
			running = False
		
		if (turning and nextDir is None):
			if (dir == "r"):
				nextDir = "l"
			elif (dir == "l"):
				nextDir = "r"
			dir = "d"
		elif (turning and nextDir is not None):
			dir = nextDir
			nextDir = None
			turning = False
		
#=== </Main> ===#


#=== <Init> ===#
if (__name__ == "__main__"):
	main()
#=== </Init> ===#