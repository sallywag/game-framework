import gameobjects
import components

class Player(gameobjects.GameObject):
	def __init__(self, location, size, tag, direction, displaysurf, sprites, current_sprite_key):
		super().__init__(location, size, tag)
		self.direction = direction
		self.collision_handler = components.CollisionHandler(self)
		self.mover = components.Mover(self)
		self.renderer = components.Renderer(self, displaysurf)
		self.shooter = components.Shooter(self)
		self.sprite_manager = components.SpriteManager(sprites, current_sprite_key)
		self.surface_cleaner = components.SurfaceCleaner(self)