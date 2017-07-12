import gameobjects

class Weapon(gameobjects.Item):
	def __init__(self, location, size, tag, ammo_type, damage, distance):
		super().__init__(location, size, tag, quantity=1)
		self.ammo_type = ammo_type
		self.damage = damage
		self.distance = distance