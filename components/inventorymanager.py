#Things to do:
#1. add_item should not check for fullness?

class InventoryManager:
	
	__slots__ = ['gameobject', 'item_locations', 'equipped_item', 'equipped_item_location', 'item_limit', 'items'] ###ADD HEALTH LOCATION
	
	def __init__(self, gameobject, item_locations, equipped_item_location, equipped_item=None):
		self.gameobject = gameobject
		self.item_locations = item_locations
		self.equipped_item_location = equipped_item_location
		self.equipped_item = equipped_item
		self.item_limit = len(item_locations)
		self.items = []
		
	def add_item(self, item):
		i = next((i for i in self.items if i.tag == item.tag), None)
		if i is not None:
			i.quantity += item.quantity
		elif not self.is_full():
			self.items.append(item)
			
	def update_item_locations(self):
		for item, item_location in zip(self.items, self.item_locations):
			item.rect.topleft = (
				self.gameobject.rect.x + item_location[0], 
				self.gameobject.rect.y + item_location[1]
			)
		if self.equipped_item is not None:
			self.equipped_item.rect.topleft = (
				self.gameobject.rect.x + self.equipped_item_location[0], 
				self.gameobject.rect.y + self.equipped_item_location[1]
			)
		
	def drop_item_at_location(self, item, drop_location):
		if item in self.items:
			item.rect.topleft = drop_location
			self.items.remove(item)
		
	def equip_item(self, item):
		if (self.equipped_item is None 
			and item.equippable 
			and item in self.items):
				self.equipped_item = item
				self.items.remove(item)
				
	def unequip_item(self):
		if self.is_full():
			self.items.append(item)
			self.equipped_item = None
				
	def remove_spent_items(self):
		for item in self.items[:]:
			if item.quantity == 0:
				self.items.remove(item)
				
	def is_full(self):
		return len(self.items) == self.item_limit