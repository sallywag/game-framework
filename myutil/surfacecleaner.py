import pygame
import itertools

class SurfaceCleaner:

	def __init__(self, displaysurf, background):
		self.displaysurf = displaysurf
		self.background = background
		self.dirty_rects = []
		self.relevant_data = {}
		
	def add(self, groups, containers):
		for group, container in itertools.zip_longest(groups, containers, fillvalue=None):
			for gameobject in group:	
				self.relevant_data[gameobject] = {
					'location' : gameobject.rect.topleft,
					'sprite' : gameobject.sprite_manager.current_sprite,
					'container' : container
				}
				
	def blit_over_dirty_rects(self):
		for gameobject, dict_ in self.relevant_data.items():
			if dict_['location'] != gameobject.rect.topleft:
				self._blit_over_gameobjects_previous_location(gameobject)
			elif dict_['sprite'] != gameobject.sprite_manager.current_sprite:
				self._blit_over_gameobject(gameobject)
			elif dict_['container'] is not None and gameobject not in dict_['container']:
				self._blit_over_gameobject(gameobject)
			self._update_relevant_data(gameobject)

	def _blit_over_gameobjects_previous_location(self, gameobject):
		self.displaysurf.blit(self.background.subsurface(gameobject), self.relevant_data[gameobject]['location'])
		self.dirty_rects.append(pygame.Rect(self.relevant_data[gameobject]['location'], gameobject.rect.size))
		self.dirty_rects.append(pygame.Rect(gameobject))
		
	def _blit_over_gameobject(self, gameobject):
		self.displaysurf.blit(self.background.subsurface(gameobject), gameobject)
		self.dirty_rects.append(pygame.Rect(gameobject))
			
	def _update_relevant_data(self, gameobject):
		self.relevant_data[gameobject]['location'] = gameobject.rect.topleft
		self.relevant_data[gameobject]['sprite'] = gameobject.sprite_manager.current_sprite_group.current_sprite
				
	def update_display(self):
		if self.dirty_rects:
			pygame.display.update(self.dirty_rects)
			self.dirty_rects = []