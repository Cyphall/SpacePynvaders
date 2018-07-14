import pygame
import SpaceInvaders
import logging

#=== <Classes> ===#
class fenetre():
	def __init__(self, size=(640, 480)):
		self.fenetre = pygame.display.set_mode(size)
		self.fenetre = pygame.display.set_caption("Space Pynvaders")
		self.spriteList = []
	
	
	def newSprite(self, path):
			self.spriteList.append(sprite(path))
	
	
	def render(self):
		for s in self.spriteList:
			s.render(self.fenetre)
		pygame.display.flip()


class sprite():
	def __init__(self, path, pos=(0, 0)):
		try:
			self.sprite = pygame.image.load(path).convert_alpha()
			self.pos = pos
			logging.info("Sprite successfully loaded from "+path)
		except Exception as e:
			logging.error(e)
			self.__destroy__()
	
	
	def setPos(self, pos):
		self.pos = pos
	
	
	def getPos(self):
		return self.pos
	
	
	def render(self, fenetre):
		fenetre.blit(self.sprite, self.pos)		
#=== </Classes> ===#


#=== <Fonctions> ===#

#=== </Fonctions> ===#


#=== <Main> ===#
def main():
	logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
	pygame.init()
	f = fenetre()
	f.newSprite("sprites/10_0.png")
	f.render()
	
	running = True
	while (running):
		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				running = False
#=== </Main> ===#


#=== <Init> ===#
if (__name__ == "__main__"):
	main()
#=== </Init> ===#