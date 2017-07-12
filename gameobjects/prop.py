import gameobjects
import components

class Prop(gameobjects.GameObject):
	def __init__(self, location, size, tag):
		super().__init__(location, size, tag)
		self.renderer = components.Renderer(self)