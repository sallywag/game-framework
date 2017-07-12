class Mover:
	'''Enables a GameObject to be moved and 
	keeps track of its previous location.
	'''
	
	__slots__ = ['gameobject']
	
	def __init__(self, gameobject):
		self.gameobject = gameobject
		
	def move(self, dx, dy):
		self.gameobject.rect.topleft = (self.gameobject.rect.x + dx, self.gameobject.rect.y + dy)