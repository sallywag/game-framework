class InventoryRenderer:
	
	__slots__ = ['gameobject', 'displaysurf', 'health', 'health_location']

	def __init__(self, gameobject, displaysurf, health, health_location):
		self.gameobject = gameobject
		self.displaysurf = displaysurf
		self.health = health
		self.health_location = health_location
	
	def draw(self):
		self.displaysurf.blit(self.gameobject.sprite_manager.get_next_sprite(), self.gameobject) #Draw inventory...
		#for item in self.gameobject.inventory_manager.items: #Draw items in inventory...
		#	self.displaysurf.blit(item.sprite_manager.get_next_sprite(), item)
		#equipped_item = self.gameobject.inventory_manager.equipped_item
		#if equipped_item is not None: #Draw equipped item...
		#	self.displaysurf.blit(equipped_item.get_next_sprite(), equipped_item)
		