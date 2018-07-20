import pygame
import logging
import os

#=== <Classes> ===#
class Display():
	def __init__(self, size=(640, 480)):
		self.display = pygame.display.set_mode(size)
		pygame.display.set_caption("Space Pynvaders")
	
	
	def render(self):
		self.display.fill((pygame.Color("black")))
		global aliens
		global player
		global shot
		for s in aliens:
			s.render(self.display)
		if (player is not None):
			player.render(self.display)
		if (shot is not None):
			shot.render(self.display)
		pygame.display.flip()
	
	
	def getDisplaySize(self):
		return {"x":pygame.display.Info().current_w, "y":pygame.display.Info().current_h} 


class Sprite():
	def __init__(self, path, pos=(0, 0)):
		try:
			self.sprite = pygame.image.load("sprites/"+str(path)).convert_alpha()
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
	

class Alien(Sprite):
	def __init__(self, path, pos=(0, 0)):
		try:
			self.sprite = [pygame.image.load(path+"_0.png").convert_alpha(), pygame.image.load(path+"_1.png").convert_alpha(), pygame.image.load("sprites/boom.png").convert_alpha()]
			self.actual = 0
			self.pos = {"x":pos[0], "y":pos[1]}
			self.size = {"x":self.sprite[0].get_size()[0], "y":self.sprite[0].get_size()[1]}
			logging.info("Sprite successfully loaded from "+path)
		except Exception as e:
			logging.error(e)
	
	
	def move(self, direction, display):
		if (self.actual == 1):
			self.actual = 0
		elif (self.actual == 0):
			self.actual = 1
		if (direction == "l"):
			self.pos["x"] -= 8
			if (self.pos["x"] <= 0):
				return True
		elif (direction == "r"):
			self.pos["x"] += 8
			if (self.pos["x"]+self.size["x"] >= display.getDisplaySize()["x"]):
				return True
		elif (direction == "d"):
			self.pos["y"] += 40
		return False
	
	
	def render(self, display):
		display.blit(self.sprite[self.actual], (self.pos["x"], self.pos["y"]))


class Player(Sprite):
	def move(self, direction, display):
		if (direction == "l"):
			self.pos["x"] -= 4
			if (self.pos["x"] < 0):
				self.pos["x"] = 0
		elif (direction == "r"):
			self.pos["x"] += 4
			if (self.pos["x"]+self.size["x"] > display.getDisplaySize()["x"]):
				self.pos["x"] = display.getDisplaySize()["x"]-self.size["x"]
	def fire(self):
		global shot
		if (shot is None):
			playSound("shoot")
			shot = Shot("shot.png", (self.pos["x"]+24, self.pos["y"]-12))


class Shot(Sprite):
	def move(self):
		self.pos["y"] -= 16
		if (self.pos["y"] < 0):
			global shot
			shot = None
			return True
		return False
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

def playSound(sound):
	global sounds
	sounds[sound].play()

def hit(alien):
	alien.actual = 2
	playSound("boom")
	global shot
	shot = None
#=== </Fonctions> ===#


#=== <Main> ===#
# Initialisation du logger #
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

os.environ['SDL_VIDEO_WINDOW_POS'] = str(200)+","+str(50)

# Initialisation de pygame #
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

# Initialisation des constantes #
FPS = 60

# Initialisation des variables #
direction = "r"
turning = False
turningOnNextLoop = False

toDelete = None
explosion = False

music = 1
timing = 0

running = True

shot = None

i = 0 # index du prochain alien à bouger

explosionFrame = 0

# initialisation des sons #
sounds = soundInit()

# Initialisation de la fenêtre #
disp = Display(size=(712, 740))

# Initialisation des aliens #
aliens = []
for y in range(5):
	for x in range(11):
		if (y == 0 or y == 1):
			temp = Alien("sprites/10")
			temp.setPos(x=x*60, y=250-y*60)
			aliens.append(temp)
		elif (y == 2 or y == 3):
			temp = Alien("sprites/20")
			temp.setPos(x=x*60, y=250-y*60)
			aliens.append(temp)
		elif (y == 4):
			temp = Alien("sprites/30")
			temp.setPos(x=x*60, y=250-y*60)
			aliens.append(temp)

# Initialisation du joueur #
player = Player("player.png")
player.setPos(y=disp.getDisplaySize()["y"]-(player.getSize()["y"]))

# Initialisation de l'horloge #
clock = pygame.time.Clock()

# Premier rendu #
disp.render()

# Boucle principale #
while (running):
	while (i < len(aliens)):
		# Évènements #
		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				running = False
		if (pygame.key.get_pressed()[97] == True or pygame.key.get_pressed()[276] == True):
			player.move("l", disp)
		if (pygame.key.get_pressed()[100] == True or pygame.key.get_pressed()[275] == True):
			player.move("r", disp)
		if (pygame.key.get_pressed()[32] == True and not explosion):
			player.fire()
		
		# Gestion du déplacement des aliens et des explosions #
		if (not explosion):
			if (turning):
				aliens[i].move("d", disp)
			else:
				if (aliens[i].move(direction, disp)):
					turningOnNextLoop = True
		else:
			explosionFrame += 1
			i -= 1
			if (explosionFrame > 20):
				explosion = False
				aliens.remove(toDelete)
				toDelete = None
				explosionFrame = 0
		
		# Gestion de la musique #
		timing += 1
		if (timing >= round(len(aliens)/1.5)+5):
			timing = 0
			playSound("music"+str(music))
			music += 1
			if (music > 4):
				music = 1
		
		# Gestion des tirs #
		if (shot is not None):
			if(not shot.move()):
				for al in aliens:
					if (collision(shot, al)):
						hit(al)
						toDelete = al
						explosion = True
						break
		
		# Gestion du rendu à l'écran #
		disp.render()
		clock.tick_busy_loop(FPS)
		
		# incrémentation de l'index des aliens #
		i += 1
	if (len(aliens) == 0):
		running = False
		
	if (turning):
		if (direction == "l"):
			direction = "r"
		else:
			direction = "l"
		turning = False
	
	if (turningOnNextLoop):
		turning = True
		turningOnNextLoop = False
	i = 0
#=== </Main> ===#