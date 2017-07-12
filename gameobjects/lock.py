import gameobjects
import components

class Lock(gameobjects.GameObject):
	def __init__(self, location, size, tag, open, key_tag, displaysurf, sprites, current_sprite, container=None):
		super().__init__(location, size, tag)
		self.open = open
		self.key_tag = key_tag
		self.renderer = components.Renderer(self, displaysurf)
		self.sprite_manager = components.SpriteManager(sprites, current_sprite)
		self.surface_cleaner = components.SurfaceCleaner(self, container)