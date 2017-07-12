import gameobjects
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
		door_sprite_sheet = myutil.load_image('images', 'door-sprite-sheet.png', (244, 244, 244))
		door_sprite_sheet = myutil.slice_sprite_sheet(door_sprite_sheet, (32, 32))
		door_sprites = [
			{'key': 'closed', 'sprites': [door_sprite_sheet[0][0]], 'max_count': 0},
			{'key': 'opening', 'sprites': [door_sprite_sheet[1][0]], 'max_count': 3},
			{'key': 'open', 'sprites': [door_sprite_sheet[2][0]], 'max_count': 3}
		]
		pistol_ammo_sprite_sheet = myutil.load_image('images/ammo', 'pistol-ammo-sprite-sheet.png', (244, 244, 244))
		pistol_ammo_sprite_sheet = myutil.slice_sprite_sheet(pistol_ammo_sprite_sheet, (32, 32))
		pistol_ammo_sprites = [
			{'key': 'default', 'sprites': [pistol_ammo_sprite_sheet[0][0]], 'max_count': 0},
			{'key': 'highlighted-far', 'sprites': [pistol_ammo_sprite_sheet[1][0]], 'max_count': 0},
			{'key': 'highlighted-yes', 'sprites': [pistol_ammo_sprite_sheet[0][1]], 'max_count': 0},
			{'key': 'highlighted-no', 'sprites': [pistol_ammo_sprite_sheet[1][1]], 'max_count': 0}
		]
		pistol_sprite_sheet = myutil.load_image('images/weapons', 'pistol-sprite-sheet.png', (244, 244, 244))
		pistol_sprite_sheet = myutil.slice_sprite_sheet(pistol_sprite_sheet, (32, 32))
		pistol_sprites = [
			{'key': 'default', 'sprites': [pistol_sprite_sheet[0][0]], 'max_count': 0},
			{'key': 'highlighted-far', 'sprites': [pistol_sprite_sheet[1][0]], 'max_count': 0},
			{'key': 'highlighted-yes', 'sprites': [pistol_sprite_sheet[0][1]], 'max_count': 0},
			{'key': 'highlighted-no', 'sprites': [pistol_sprite_sheet[1][1]], 'max_count': 0}
		]
		self.background_img = myutil.load_image('images', 'background.png')
		inventory_img = myutil.load_image('images', 'inventory.png')
		#-------#
		
		#---------#
		#INVENTORY#
		#---------#
		self.player_inventory = gameobjects.Inventory(
			location=(0, 0), 
			size=(160, 64), 
			tag='inventory-player', 
			item_locations=[
				(0, 0), (32, 0), (64, 0), (96, 0),
				(0, 32), (32, 32), (64, 32), (96, 32)
			], 
			equipped_item_location=(128, 0),
			equipped_item=None, 
			displaysurf=self.displaysurf, 
			health=100,
			sprites=[{'key': 'inventory', 'sprites': [inventory_img], 'max_count': 0}],
			current_sprite_key='inventory'
		)
		#---------#
		
		#----------#
		#CONTAINERS#
		#----------#
		self.blockers = [
			gameobjects.Lock(myutil.cc(5, 4, 32), (32, 32), 'lock', False, None, self.displaysurf, door_sprites, 'closed'),
			gameobjects.Lock(myutil.cc(5, 7, 32), (32, 32), 'lock', False, None, self.displaysurf, door_sprites, 'closed'),
			gameobjects.Lock(myutil.cc(9, 2, 32), (32, 32), 'lock', False, None, self.displaysurf, door_sprites, 'closed'),
		]
		self.blockers.append(gameobjects.Lock(myutil.cc(14, 2, 32), (32, 32), 'click', False, None, self.displaysurf, door_sprites, 'closed', self.blockers))
		self.items = [
			gameobjects.Item((192, 32), (32, 32), 'pistol', 1, True, self.displaysurf, pistol_sprites, 'default'),
			gameobjects.Item((192, 64), (32, 32), 'pistol-ammo-1', 10, False, self.displaysurf, pistol_ammo_sprites, 'default'),
			gameobjects.Item((192, 96), (32, 32), 'pistol-ammo-2', 10, False, self.displaysurf, pistol_ammo_sprites, 'default'),
			gameobjects.Item((192, 128), (32, 32), 'pistol-ammo-3', 10, False, self.displaysurf, pistol_ammo_sprites, 'default'),
			gameobjects.Item((192, 160), (32, 32), 'pistol-ammo-4', 10, False, self.displaysurf, pistol_ammo_sprites, 'default'),
			gameobjects.Item((192, 192), (32, 32), 'pistol-ammo-5', 10, False, self.displaysurf, pistol_ammo_sprites, 'default'),
			gameobjects.Item((192, 224), (32, 32), 'pistol-ammo-6', 10, False, self.displaysurf, pistol_ammo_sprites, 'default'),
			gameobjects.Item((192, 256), (32, 32), 'pistol-ammo-7', 10, False, self.displaysurf, pistol_ammo_sprites, 'default'),
			gameobjects.Item((192, 288), (32, 32), 'pistol-ammo-8', 10, False, self.displaysurf, pistol_ammo_sprites, 'default')
		]
		self.enemies = []
		self.things_to_draw = []
		self.things_not_to_draw = []
		#----------#
		
		#------#
		#PLAYER#
		#------#
		self.player = gameobjects.Player((128, 128), (32, 32), 'player', myutil.Constants.down, self.displaysurf, player_sprites, 'down-idle')
		#------#
		
		#---------------#
		#SURFACE CLEANER#
		#---------------#
		self.surface_cleaner = myutil.SurfaceCleaner(self.displaysurf, self.background_img)
		self.surface_cleaner.add([self.items, self.blockers, [self.player]], [None, self.blockers])
		#---------------#
		
		self.time_to_wait = 0
		self.just_loaded = True
		self.displaysurf.blit(self.background_img, (0, 0))
	
	def input(self):
		myutil.InputManager.get_events()
		myutil.InputManager.check_for_quit_event()
		myutil.InputManager.update_keyboard_key_state()
		myutil.InputManager.get_keyboard_input()
		myutil.InputManager.update_mouse_button_state()
		myutil.InputManager.get_mouse_input()

	def update(self):
		#--------------#
		#SET COLLISIONS#
		#--------------#
		self.player.collision_handler.set_collisions(['items'], [self.items])
		#player_moveable_interactor.collision_handler.set_collisions(['moveables'], [moveables])
		#--------------#
	
		if self.time_to_wait == 0:
			if (myutil.InputManager.keyboard[pygame.K_UP] == 'held'
				or myutil.InputManager.keyboard[pygame.K_UP] == 'pressed'):
					if self.player.rect.topleft[1] != 0:
						self.player.direction = myutil.Constants.up
						self.player.sprite_manager.set_sprite_group('up')
						self.player.mover.move(0, -2)
			elif (myutil.InputManager.keyboard[pygame.K_DOWN] == 'held'
					or myutil.InputManager.keyboard[pygame.K_DOWN] == 'pressed'):
						if self.player.rect.bottomright[1] != self.screen_size[1]:
							self.player.direction = myutil.Constants.down
							self.player.sprite_manager.set_sprite_group('down')
							self.player.mover.move(0, 2)
			elif (myutil.InputManager.keyboard[pygame.K_LEFT] == 'held'
					or myutil.InputManager.keyboard[pygame.K_LEFT] == 'pressed'):
						if self.player.rect.topleft[0] != 0:
							self.player.direction = myutil.Constants.left
							self.player.sprite_manager.set_sprite_group('left')
							self.player.mover.move(-2, 0)
			elif (myutil.InputManager.keyboard[pygame.K_RIGHT] == 'held'
					or myutil.InputManager.keyboard[pygame.K_RIGHT] == 'pressed'):
						if self.player.rect.bottomright[0] != self.screen_size[0]:
							self.player.direction = myutil.Constants.right
							self.player.sprite_manager.set_sprite_group('right')
							self.player.mover.move(2, 0)
			else:
				self.player.sprite_manager.set_sprite_group('{}-idle'.format(self.player.direction))
				
			#---------------#
			#HIGHLIGHT ITEMS#
			#---------------#
			for item in set(self.items+self.player_inventory.inventory_manager.items):
				if item.rect.collidepoint(myutil.InputManager.cursor_location):
					if item in self.player.collision_handler.collisions['items']:
						if not self.player_inventory.inventory_manager.is_full():
							item.sprite_manager.set_sprite_group('highlighted-yes')
						else:
							item.sprite_manager.set_sprite_group('highlighted-no')
					else:
						item.sprite_manager.set_sprite_group('highlighted-far')
				else: 
					item.sprite_manager.set_sprite_group('default')
			#---------------#
			
			#------------------#
			#EQUIP/UNEQUIP ITEM#
			#------------------#
			for item in self.player_inventory.inventory_manager.items:
				if item.rect.collidepoint(myutil.InputManager.cursor_location):
					if myutil.InputManager.mouse[3] == 'pressed':
						if item.equippable:
							self.player_inventory.inventory_manager.equip_item(item) ###NOT DRAWING HOW ARE WE HANDLING DRAWING?
			#------------------#
			
			#------------------#
			#PICK UP/DROP ITEMS#
			#------------------#
			for item in set(self.items+self.player_inventory.inventory_manager.items):
				if item.rect.collidepoint(myutil.InputManager.cursor_location):
					if myutil.InputManager.mouse[1] == 'pressed':
						if item in self.player_inventory.inventory_manager.items:
							self.items.append(self.player_inventory.inventory_manager.drop_item_at_location(item, self.player.rect.topleft))
						elif item in self.player.collision_handler.collisions['items']:
							self.player_inventory.inventory_manager.add_item(item)
							self.items.remove(item)###
			#------------------#
			
			print(self.player_inventory.inventory_manager.equipped_item)
			
			if myutil.InputManager.quit:
				myutil.terminate()
				
			#if myutil.InputManager.keyboard[pygame.K_SPACE] == 'pressed':
			#	self.player.sprite_manager.add_to_reel('shoot')
			#	self.time_to_wait += 60
			#elif myutil.InputManager.keyboard[pygame.K_d] == 'pressed':
			#	if self.player_inventory.inventory_manager.items:
			#		self.items.append(self.player_inventory.inventory_manager.drop_item(
			#			self.player_inventory.inventory_manager.items[0], 
			#		self.player.rect.topleft)
			#		)
			#	else:
			#		self.player_inventory.inventory_manager.add_item(self.items.pop(0))
		#	if myutil.InputManager.keyboard[pygame.K_SPACE]: ###BUG HERE UP AND DOWN PRODUCES 2 EVENTS!!!! NEED INPUT MANAGER USING EVENTS QUEUE???!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
				#print('here')
				#self.player.sprite_manager.add_to_reel('shoot')
				#self.time_to_wait += 60
				
				#if event.type == pygame.QUIT:
				#	myutil.terminate()
				#elif myutil.InputManager.keyboard[pygame.K_i]:
				#	self.inventory_open = not self.inventory_open
			#	elif myutil.InputManager.keyboard[pygame.K_d] == 'pressed':
					#if self.player_inventory.inventory_manager.items:
					#	self.items.append(self.player_inventory.inventory_manager.drop_item(
					#		self.player_inventory.inventory_manager.items[0], 
					#		self.player.rect.topleft)
					#	)
					#else:
					#	self.player_inventory.inventory_manager.add_item(self.items.pop(0))
					
		self.player_inventory.inventory_manager.update_item_locations()
		if pygame.mouse.get_pressed()[0]:
			for blocker in self.blockers[:]:
				if blocker.rect.collidepoint(pygame.mouse.get_pos()) and not blocker.open and blocker.tag != 'click': ###NEED STATES TO PREVENT MULTIPLE CLICKS!
					blocker.open = not blocker.open
					blocker.sprite_manager.add_to_reel('opening') ### 
					blocker.sprite_manager.set_sprite_group('open') 
				elif blocker.rect.collidepoint(pygame.mouse.get_pos()) and blocker.tag == 'click':
					self.blockers.remove(blocker)

	
	def render(self):
		self.surface_cleaner.blit_over_dirty_rects()
		for blocker in self.blockers:
			blocker.renderer.draw()
		self.player_inventory.inventory_renderer.draw()
		for item in self.items:
			item.renderer.draw()
		for item in self.player_inventory.inventory_manager.items:
			item.renderer.draw()
		self.surface_cleaner.dirty_rects.append(self.player_inventory)
		self.player.renderer.draw()
		if self.just_loaded: 
			pygame.display.update()
			self.just_loaded = not self.just_loaded
		else:
			self.surface_cleaner.update_display()
			
	def mainloop(self):
		while True:
			self.input()
			self.update()
			self.render()
			if self.time_to_wait > 0:
				self.time_to_wait -= 1
			self.player.collisions = {}	
			self.fps_clock.tick(self.fps)
	
if __name__ == '__main__':
	game = Game()
	game.mainloop()