import pygame

class GameObject:
	
	def __init__(self, location, size, tag):
		self.rect = pygame.Rect(location, size)
		self.tag = tag
		
	def __str__(self):
		return '{class_}, location: {rect.topleft}, size: {rect.size}'.format(class_=self.__class__, rect=self.rect)