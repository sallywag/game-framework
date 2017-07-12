import gameobjects
import components

class Bullet(gameobjects.GameObject):
	def __init__(self, location, size, tag, damage, distance, direction):
		super().__init__(location, size, tag)
		self.damage = damage
		self.distance = distance
		self.direction = direction
		self.mover = components.Mover(self)
		self.renderer = components.Renderer(self)