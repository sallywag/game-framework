import gameobjects
import components

class Enemy(gameobjects.GameObject):
	def __init__(self, location, size, tag, direction, move_speed, health):
		super().__init__(location, size, tag)
		self.direction = direction
		self.health = health
		self.mover = components.Mover(self)
		self.renderer = components.Renderer(self)
		self.shooter = components.Shooter(self)