import gameobjects
import myutil

import pygame

import time

#---------#
#CONSTANTS#
#---------#
CELL_SIZE = 32
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
PUSHING = 'pushing' 
WEAPON_READY = 'weapon_ready'
#---------#

#-----#
#NOTES#
#-----#
###ONLY use set collisions if the collisions will be tested more than once
 ### - Where should the code go?
#1. Is there a better way to do bullets/weapons/ammo/shooter stuff?
#2. Should functionality be tied to an object if it is only used by that object?
#3. Remember not to update the whole screen when you get to sprites.
#4. Should Player and Enemy inherit from something else.
#5. Fix that you use gameobject instead of gameobject.rect.
#6. Use collision_handler when you want to reuse the same collisions in one frame.
#-----#

def main():
	pygame.init()
	pygame.display.set_caption('Horror Game Dev!')
	screen_size = (640, 480)
	displaysurf = pygame.display.set_mode(screen_size)
	fps_clock = pygame.time.Clock()
	fps = 30

	#-----#
	#ITEMS#
	#-----#
	key = gameobjects.Item((160, 160), (32, 32), 'key', 1)
	#-----#
	
	#-------#
	#WEAPONS#
	#-------#
	pistol = gameobjects.Weapon((96, 96), (32, 32), 'pistol', 'ammo-pistol', 25, 20)
	axe = gameobjects.Weapon((160, 96), (32, 32), 'axe', None, 10, 1)
	#-------#
	
	#----#
	#AMMO#
	#----#
	pistol_ammo = gameobjects.Item((96, 96), (32, 32), 'ammo-pistol', 15)
	#----#
	
	#------#
	#PLAYER#
	#------#
	player = gameobjects.Player((0, 0), (32, 32), 'player', DOWN, 2)
	player_interactor = gameobjects.Interactor((player.rect.x - 32, player.rect.y - 32), (96, 96), 'player-interactor')
	player_moveable_interactor = gameobjects.Interactor((player.rect.x - 4, player.rect.y - 4), (40, 40), 'player-moveable-interactor')
	player_inventory = gameobjects.Inventory((0, 0), (0, 0), 'inventory-player', [pistol_ammo, key], 8, pistol)
	#------#
	
	blockers = [
	#	gameobjects.Prop((96, 128), (32, 32), 'lock'),
		#gameobjects.Prop((64, 128), (32, 32), 'lock'),
		gameobjects.MoveableProp((128, 256), (32, 32), 'moveable')
	]
	moveables = [blocker for blocker in blockers if blocker.tag == 'moveable']
	enemies = [
		#gameobjects.Enemy((128, 128), (32, 32), 'zombie', LEFT, 2, 100),
		#gameobjects.Enemy((160, 128), (32, 32), 'zombie', LEFT, 2, 50)
	]
	bullets = []
	
	while True:
		pygame.event.pump()
	
		##-----##
		##INPUT##
		##-----##
		keyboard = pygame.key.get_pressed()
		##-----##
		
		##------##
		##UPDATE##
		##------##
		
		#--------------#
		#SET COLLISIONS#
		#--------------#
		player_interactor.collision_handler.set_collisions(['blockers'], [blockers])
		player_moveable_interactor.collision_handler.set_collisions(['moveables'], [moveables])
		#--------------#
		
		if keyboard[pygame.K_UP]:
			player.direction = UP
			player.mover.move(0, -player.move_speed)
			if player.rect.topleft[1] < 0:
				player.mover.move(0, player.move_speed)
		elif keyboard[pygame.K_DOWN]:
			player.direction = DOWN
			player.mover.move(0, player.move_speed)
			if player.rect.bottomright[1] > screen_size[1]:
				player.mover.move(0, -player.move_speed)
		elif keyboard[pygame.K_LEFT]:
			player.direction = LEFT
			player.mover.move(-player.move_speed, 0)
			if player.rect.topleft[0] < 0:
				player.mover.move(player.move_speed, 0)
		elif keyboard[pygame.K_RIGHT]:
			player.direction = RIGHT
			player.mover.move(player.move_speed, 0)
			if player.rect.bottomright[0] > screen_size[0]:
				player.mover.move(-player.move_speed, 0)
				
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				myutil.terminate()
			elif event.type == pygame.KEYDOWN:
				#-----#
				#SHOOT#
				#-----#
				if event.key == pygame.K_SPACE:
					bullet = player.shooter.shoot(player_inventory)
					if bullet is not None:
						bullets.append(bullet)
				#-----#
				elif event.key == pygame.K_e:
					pass
			elif event.type == pygame.MOUSEBUTTONDOWN:
				#----------#
				#OPEN LOCKS#
				#----------#
				if event.button == 1:
					try:
						for blocker in player_interactor.collision_handler.collisions['blockers']:
							if blocker.rect.collidepoint(event.pos):
								if blocker.tag == 'lock' and 'key' in player_inventory:
									item = player_inventory.inventory_manager.get_item_by_tag('key') ###
									item.quantity -= 1 ###
									blockers.remove(blocker)
					except KeyError: pass
				#----------#
		
		#=---------------------------------------------#
		#MOVE OR REMOVE BULLETS, DAMAGE OR KILL ENEMIES#
		#----------------------------------------------#
		for bullet in bullets:
			index = bullet.rect.collidelist(enemies)
			if index != -1: 
				enemies[index].health -= bullet.damage
				if enemies[index].health <= 0: enemies.remove(enemies[index]) ###
				bullets.remove(bullet)
			elif (bullet.distance == 0
				or bullet.rect.x < 0 or bullet.rect.x > screen_size[0]
				or bullet.rect.y < 0 or bullet.rect.y > screen_size[1]
				or bullet.rect.collidelist(blockers) != -1):
					bullets.remove(bullet)
			else:
				if bullet.direction == UP: bullet.mover.move(0, -32)
				if bullet.direction == DOWN: bullet.mover.move(0, 32)
				if bullet.direction == LEFT: bullet.mover.move(-32, 0)
				if bullet.direction == RIGHT: bullet.mover.move(32, 0)
				bullet.distance -= 1
		#----------------------------------------------#
		
		#--------------#
		#SET COLLISIONS#
		#--------------#
		player.collision_handler.set_collisions(['blockers', 'moveables'], [blockers])
		#--------------#
		
		#---------------------#
		#COLLIDE WITH BLOCKERS#
		#---------------------#
		try: ###FIX USE TRY EXCEPT ELSEon == DOWN: 
						if player.rect.centerx < collider.centerx - (collider.centerx - collider.topleft[0]):
							player.mover.move(-player.move_speed, 0)
						elif player.rect.centerx > collider.centerx + (collider.topright[0] - collider.centerx):
							player.mover.move(player.move_speed, 0)
					elif player.direction == LEFT or player.direction == RIGHT:
						if player.rect.centery < collider.centery - (collider.centery - collider.topleft[1]):
							player.mover.move(0, -player.move_speed)
						elif player.rect.centery > collider.centery + (collider.bottomright[1] - collider.centery ):
							player.mover.move(0, player.move_speed)
		except KeyError: pass
		#---------------------#
		##------##
		
		##----##
		##DRAW##
		##----##
		displaysurf.fill(myutil.Colors.BLACK)
		pygame.draw.rect(displaysurf, myutil.Colors.PINK, player_moveable_interactor)
		player.renderer.draw(displaysurf, myutil.Colors.GREEN)
		for enemy in enemies:
			enemy.renderer.draw(displaysurf, myutil.Colors.RED)
		for blocker in blockers:
			blocker.renderer.draw(displaysurf, myutil.Colors.GRAY)
		for bullet in bullets:
			bullet.renderer.draw(displaysurf, myutil.Colors.BLUE)
		##----##
		
		#------#
		#UPKEEP#
		#------#
		player_interactor.rect.topleft = (player.rect.x - 32, player.rect.y - 32)
		player_moveable_interactor.rect.topleft = (player.rect.x - 4, player.rect.y - 4)
		player_inventory.inventory_manager.clean_up() ###
		player.collision_handler.collisions = {}
		player_interactor.collision_handler.collisions = {}
		pygame.display.update()
		fps_clock.tick(fps)
		#------#
	
if __name__ == '__main__':
	main()