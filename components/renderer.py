class Renderer:
	'''Enables a GameObject to be drawn.'''
	
	__slots__ = ['gameobject', 'displaysurf']

	def __init__(self, gameobject, displaysurf):
		self.gameobject = gameobject
		self.displaysurf = displaysurf
	
	def draw(self):
		self.displaysurf.blit(self.gameobject.sprite_manager.get_next_sprite(), self.gameobject)