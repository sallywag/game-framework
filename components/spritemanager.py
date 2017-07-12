import myutil
import itertools

#Should a single sprite not be a sprite group?

class SpriteManager:

	__slots__ = ['sprites', 'current_sprite_group', 'reel']
	
	def __init__(self, dicts, current_sprite_group_key):
		self.sprites = {}
		for dict_ in dicts:
			self.sprites[dict_['key']] = SpriteGroup(dict_['sprites'], dict_['max_count'])											
		self.current_sprite_group = self.sprites[current_sprite_group_key]
		self.reel = []
		
	@property
	def current_sprite(self):
		return self.current_sprite_group.current_sprite
	
	def get_next_sprite(self):
		if self.reel:
			self.current_sprite_group.current_sprite = self.reel.pop(0)
			return self.current_sprite_group.current_sprite
		return self.current_sprite_group.get_next_sprite()
		
	def set_sprite_group(self, key):
		if self.current_sprite_group != self.sprites[key]:
			self.current_sprite_group = self.sprites[key]
			self.current_sprite_group.reset()
		
	def add_to_reel(self, key):
		for i in range(len(self.sprites[key].sprites)):
			self.reel.append(self.sprites[key].sprites[i])
			for j in range(self.sprites[key].max_count): #Add spacing between each sprite if needed...
				self.reel.append(self.sprites[key].sprites[i])

class SpriteGroup:

	def __init__(self, sprites, max_count):
		self.sprites = sprites
		self.max_count = max_count
		self.current_count = self.max_count
		self.sprite_reel = itertools.cycle(sprites)
		self.current_sprite = sprites[0] ###DO YOU NEED THIS??
		
	def get_next_sprite(self):
		if self.current_count == self.max_count: 
			self.current_count = 0
			self.current_sprite = next(self.sprite_reel) ###WILL GET THE FIRST SPRITE NOT THE SECOND
		else: 
			self.current_count += 1
		return self.current_sprite
		 
	def reset(self):
		self.current_count = self.max_count
		self.sprite_reel = itertools.cycle(self.sprites)
		self.current_sprite = self.sprites[0] ###DO YOU NEED THIS??