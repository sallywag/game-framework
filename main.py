import gameobjects
import components
import myutil
import pygame
import time

###Things to do:
###2. myutil.blit_over(displaysurf, gameobject, surface) replace with something similar to surface cleaner because
###transpartent background require multiple blit overs
###3. simplify sprite manager too many steps to complex
###Remove bullet creation from shoot component to avoid circular ref?
###4. Simplify Surface Cleaner.

###Learn:
###1. def func(arg1, arg2, arg3, *, kwarg1, kwarg2): 

"""Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
"""

class Game:

	def __init__(self):
		pygame.init()
		pygame.display.set_caption('Horror Game Dev!')
		self.screen_size = (640, 480)
		self.displaysurf = pygame.display.set_mode(self.screen_size)
		self.fps_clock = pygame.time.Clock()
		self.fps = 30
		#-------#
		#SPRITES#
		#-------#
		player_sprite_sheet = myutil.load_image('images', 'player-sprite-sheet.png', (244, 244, 244))
		player_sprite_sheet = myutil.slice_sprite_sheet(player_sprite_sheet, (32, 32))
		player_shoot_sprite_sheet = myutil.load_image('images', 'player-shoot-sprite-sheet.png')
		player_shoot_sprite_sheet = myutil.slice_sprite_sheet(player_shoot_sprite_sheet, (32, 32))
		door_sprite_sheet = myutil.load_image('images', 'door-sprite-sheet.png', (244, 244, 244))
		door_sprite_sheet = myutil.slice_sprite_sheet(door_sprite_sheet, (32, 32))
		player_sprites = [
			{'key': 'up', 'sprites': [player_sprite_sheet[1][2], player_sprite_sheet[2][2], player_sprite_sheet[3][2], player_sprite_sheet[4][2]], 'max_count': 3},
			{'key': 'up-idle', 'sprites': [player_sprite_sheet[0][2]], 'max_count': 0},
			{'key': 'down', 'sprites': [player_sprite_sheet[1][0], player_sprite_sheet[2][0], player_sprite_sheet[3][0], player_sprite_sheet[4][0]], 'max_count': 3},
			{'key': 'down-idle', 'sprites': [player_sprite_sheet[0][0]], 'max_count': 0},
			{'key': 'left', 'sprites': [player_sprite_sheet[1][1], player_sprite_sheet[2][1], player_sprite_sheet[3][1], player_sprite_sheet[4][1]], 'max_count': 3},
			{'key': 'left-idle', 'sprites': [player_sprite_sheet[0][1]], 'max_count': 0},
			{'key': 'right', 'sprites': [player_sprite_sheet[1][3], player_sprite_sheet[2][3], player_sprite_sheet[3][3], player_sprite_sheet[4][3]], 'max_count': 3},
			{'key': 'right-idle', 'sprites': [player_sprite_sheet[0][3]], 'max_count': 0},
			{'key': 'shoot', 'sprites': [player_shoot_sprite_sheet[0][0], player_shoot_sprite_sheet[1][0], player_shoot_sprite_sheet[2][0]], 'max_count': 19}
		]
		door_sprites = [
			{'key': 'closed', 'sprites': [door_sprite_sheet[0][0]], 'max_count': 0},
			{'key': 'opening', 'sprites': [door_sprite_sheet[1][0]], 'max_count': 3},
			{'key': 'open', 'sprites': [door_sprite_sheet[2][0]], 'max_count': 3}
		]
		#-------#
		self.player = gameobjects.Player((0, 0), (32, 32), 'player', myutil.Constants.down, self.displaysurf, player_sprites, 'down-idle')
		self.inventory_img = myutil.load_image('images', 'brick.png')
		self.background_img = myutil.load_image('images', 'background.png')
		self.time_to_wait = 0
		self.blockers = [
			gameobjects.Lock(myutil.cc(5, 4, 32), (32, 32), 'lock', False, None, self.displaysurf, door_sprites, 'closed'),
			gameobjects.Lock(myutil.cc(5, 7, 32), (32, 32), 'lock', False, None, self.displaysurf, door_sprites, 'closed'),
			gameobjects.Lock(myutil.cc(9, 2, 32), (32, 32), 'lock', False, None, self.displaysurf, door_sprites, 'closed'),
		]
		self.blockers.append(gameobjects.Lock(myutil.cc(14, 2, 32), (32, 32), 'click', False, None, self.displaysurf, door_sprites, 'closed', self.blockers))
		self.inventory_open = False
		self.just_loaded = True
		self.displaysurf.blit(self.background_img, (0, 0))

	def input(self):
		pygame.event.pump()
		keyboard = pygame.key.get_pressed()
		if self.time_to_wait == 0:
			if keyboard[pygame.K_UP]:
				if self.player.rect.topleft[1] != 0:
					self.player.direction = myutil.Constants.up
					self.player.sprite_manager.set_sprite_group('up')
					self.player.mover.move(0, -2)
			elif keyboard[pygame.K_DOWN]:
				if self.player.rect.bottomright[1] != self.screen_size[1]:
					self.player.direction = myutil.Constants.down
					self.player.sprite_manager.set_sprite_group('down')
					self.player.mover.move(0, 2)
			elif keyboard[pygame.K_LEFT]:
				if self.player.rect.topleft[0] != 0:
					self.player.direction = myutil.Constants.left
					self.player.sprite_manager.set_sprite_group('left')
					self.player.mover.move(-2, 0)
			elif keyboard[pygame.K_RIGHT]:
				if self.player.rect.bottomright[0] != self.screen_size[0]:
					self.player.direction = myutil.Constants.right
					self.player.sprite_manager.set_sprite_group('right')
					self.player.mover.move(2, 0)
			else:
				self.player.sprite_manager.set_sprite_group('{}-idle'.format(self.player.direction))
			if keyboard[pygame.K_SPACE]:
				self.player.sprite_manager.add_to_reel('shoot')
				self.time_to_wait += 60
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					myutil.terminate()
				elif keyboard[pygame.K_i]:
					self.inventory_open = not self.inventory_open

	def update(self):
		###PICK UP ITEM OPEN LOCK DRAW TEST###
		if pygame.mouse.get_pressed()[0]:
			for blocker in self.blockers:
				if blocker.rect.collidepoint(pygame.mouse.get_pos()) and not blocker.open and blocker.tag != 'click': ###NEED STATES TO PREVENT MULTIPLE CLICKS!
					blocker.open = not blocker.open
					blocker.sprite_manager.add_to_reel('opening') ### 
					blocker.sprite_manager.set_sprite_group('open') 
				elif blocker.tag == 'click':
					blockers.remove(blocker)
					blocker.surface_cleaner.queue_for_cleaning(self.displaysurf, self.background_img)
	
	def render(self):
		self.player.surface_cleaner.queue_for_cleaning(self.displaysurf, self.background_img)
		for blocker in self.blockers:
			blocker.surface_cleaner.queue_for_cleaning(self.displaysurf, self.background_img)
			blocker.renderer.draw()
		self.player.renderer.draw()

	def mainloop(self):
		while True:
			self.input()
			self.update()
			self.render()
			if self.time_to_wait > 0:
				self.time_to_wait -= 1
			if self.just_loaded: 
				pygame.display.update()
				self.just_loaded = not self.just_loaded
			else:
				components.SurfaceCleaner.clean(self.displaysurf)	
			self.player.collisions = {}	
			self.fps_clock.tick(self.fps)
	
if __name__ == '__main__':
	game = Game()
	game.mainloop()