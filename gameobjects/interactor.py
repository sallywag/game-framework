import gameobjects
import components

class Interactor(gameobjects.GameObject):
	'''A simple gameobject with collision and nothing else.'''

	def __init__(self, location, size, tag):
		super().__init__(location, size, tag)
		self.collision_handler = components.CollisionHandler(self)