import components

class ProjectileMover(components.Mover):
	
	__slots__ = ['projectile']
	
	def __init__(self, projectile):
		super().__init__(projectile)
		
	def move(self, x_offset, y_offset): ###???? SHOULD DI RECTION TEST BE IN REGULAR MOVER COMPONENT
		if self.gameobject.distance > 0:
			if self.gameobject.direction == UP: super().move(0, -y_offset)
			elif self.gameobject.direction == DOWN: super().move(0, y_offset)
			elif self.gameobject.direction == LEFT: super().move(-x_offset, 0)
			elif self.gameobject.direction == RIGHT: super().move(x_offset, 0)
			self.gameobject.distance -= 1