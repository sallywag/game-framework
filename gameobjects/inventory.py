import gameobjects
import components

class Inventory(gameobjects.GameObject):
	
	def __init__(self, location, size, tag, item_locations, equipped_item_location, equipped_item, displaysurf, health, sprites, current_sprite_key):
		super().__init__(location, size, tag)
		self.inventory_manager = components.InventoryManager(self, item_locations, equipped_item_location, equipped_item)
		self.inventory_renderer = components.InventoryRenderer(self, displaysurf, health)
		self.sprite_manager = components.SpriteManager(sprites, current_sprite_key)