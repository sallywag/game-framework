import gameobjects
import components
import pygame

class Text(gameobjects.GameObject):
	
	def __init__(self, size, text, color, displaysurf, background=None, antialias=None, bold=False, italic=False):
		self.font = pygame.font.SysFont(name=None, size=size, bold=bold, italic=italic)
		self.text = render(text=text, antialias=antialias, color=color, background=background)
		self.renderer = components.TextRenderer(self, displaysurf)
		super.__init__(text.get_rect())