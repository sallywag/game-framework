class TextRenderer:
	
	__slots__ = ['gameobject', 'displaysurf']

	def __init__(self, gameobject, displaysurf):
		self.gameobject = gameobject
		self.displaysurf = displaysurf
	
	def draw(self):
		self.displaysurf.blit(self.gameobject.text, self.gameobject)