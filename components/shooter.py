class Shooter:
	'''Enables a GameObject to shoot if a weapon is equipped and
	the proper ammunition exists in its inventory.
	'''
	###FIX NO MORE BULLET IMPORT
	__slots__ = ['gameobject']

	def __init__(self, gameobject):
		self.gameobject = gameobject
		
	def shoot(self, inventory):
		#No ammunition required...
		if inventory.equipped_item.ammo_type is None:
			return gameobjects.Bullet(
				self.gameobject.rect.topleft, 
				self.gameobject.rect.size, 
				'bullet-{}'.format(inventory.equipped_item.tag), 
				inventory.equipped_item.damage, 
				inventory.equipped_item.distance, 
				self.gameobject.direction
			)
		#Ammunition required...
		else:
			for item in inventory.items:
				if inventory.equipped_item.ammo_type == item.tag:
					item.quantity -= 1
					return gameobjects.Bullet(
						self.gameobject.rect.topleft, 
						self.gameobject.rect.size, 
						'bullet-{}'.format(inventory.equipped_item.tag), 
						inventory.equipped_item.damage, 
						inventory.equipped_item.distance, 
						self.gameobject.direction
					)
			return None