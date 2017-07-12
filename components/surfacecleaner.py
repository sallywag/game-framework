import pygame

#1. Should not be component?
#2. queue_for_cleaning does too much?
#3. queue_for_cleaning/clean poorly named?
#4. THIS COMPONENT IS TEMPORARY OR NEEDS REVISION HANDLES TOO MUCH.

class SurfaceCleaner:

	dirty_rects = []
	
	__slots__ = ['gameobject', 'location', 'sprite', 'container']

	def __init__(self, gameobject, container=None):
		self.gameobject = gameobject
		self.location = gameobject.rect.topleft
		if self.gameobject.sprite_manager.reel:
			self.sprite = self.gameobject.sprite_manager.reel[0]
		else:
			self.sprite = self.gameobject.sprite_manager.current_sprite_group.current_sprite
		self.container = container

	@classmethod
	def clean(cls, display):
		if cls.dirty_rects:
			pygame.display.update(cls.dirty_rects)
			cls.dirty_rects = []

	def queue_for_cleaning(self, display, surface): #Handles too mucb?
		if self.location != self.gameobject.rect.topleft: #Gameobject has been moved...
			display.blit(surface.subsurface(self.gameobject), self.location)
			self.dirty_rects.append(pygame.Rect(self.location, self.gameobject.rect.size))
			self.dirty_rects.append(pygame.Rect(self.gameobject))
		elif self.sprite != self.gameobject.sprite_manager.current_sprite_group.current_sprite: #Sprite has been changed...
			display.blit(surface.subsurface(self.gameobject), self.gameobject)
			self.dirty_rects.append(pygame.Rect(self.gameobject)) ###Should be gameobject.rect, just gameobject, or Rect(gameobject)???
		elif self.container is not None and self.gameobject not in self.container: #Gameobject has been removed from the container... ###!!!SHOULD NOT CHECK FOR SELF CONTAINER???
			display.blit(surface.subsurface(self.gameobject), self.gameobject)
			self.dirty_rects.append(pygame.Rect(self.gameobject))
			
		self.location = self.gameobject.rect.topleft
		if self.gameobject.sprite_manager.reel:
			self.sprite = self.gameobject.sprite_manager.reel[0]
		else:
			self.sprite = self.gameobject.sprite_manager.current_sprite_group.current_sprite