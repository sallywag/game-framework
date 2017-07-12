#Things to do:
#1. New docstrings.
#2. Unit tests.

class CollisionHandler:
	
	__slots__ = ['gameobject', 'collisions']
	
	def __init__(self, gameobject):
		self.gameobject = gameobject
		self.collisions = {}
		
	def set_collisions(self, keys, groups):
		for key, group in zip(keys, groups):
			self.collisions[key] = []
			indexes = self.gameobject.rect.collidelistall(group)
			if indexes: 
				self.collisions[key] = [group[index] for index in indexes]
				
	def set_collision(self, keys, groups):
		for key, group in zip(keys, groups):
			if self.gameobject.rect.collidelist(group) != -1:
				self.collisions[key] = group[self.gameobject.rect.collidelist(group)]