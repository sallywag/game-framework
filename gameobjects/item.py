import gameobjects
import components

class Item(gameobjects.GameObject):
	def __init__(self, location, size, tag, quantity, equippable, displaysurf, sprites, current_sprite_key):
		super().__init__(location, size, tag)
		self.quantity = quantity
		self.equippable = equippable
		self.renderer = components.Renderer(self, displaysurf)
		self.sprite_manager = components.SpriteManager(sprites, current_sprite_key)