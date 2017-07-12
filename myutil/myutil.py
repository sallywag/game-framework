import os
import sys
import pygame

class Colors:

	black = (0, 0, 0)
	white = (255, 255, 255)
	gray = (96, 96, 96) 
	red = (255, 0, 0)
	green = (0, 255, 0)
	blue = (0, 0, 255)
	purple = (255, 0, 255)
	yellow = (255, 255, 0)
	orange = (255,165,0)
	aqua = (0, 255, 255)
	brown = (165, 42, 42)
	pink = (255, 192, 203)
	colorkey = (244, 244, 244)

class States:

	standing = 'standing'
	moving = 'moving'
	shooting = 'shooting'
	open = 'open'
	closed = 'closed'
	
class Constants:

	up = 'up'
	down = 'down'
	left = 'left'
	right = 'right'

def terminate():
	pygame.quit()
	sys.exit()
	
def cc(x, y, cell_size):
	return (x * cell_size, y * cell_size)
	
def load_image(directory, file_name, colorkey=None):
	image = pygame.image.load(os.path.join(directory, file_name)).convert()
	if colorkey is not None:
		image.set_colorkey(colorkey)
	return image
	
def load_images_from_directory(directory, extensions):
	'''Yield the file name (no extension) and image for all files in 
	the given directory that have the desired extension(s).
	'''
	
	for item in os.listdir(directory):
		if (os.path.isfile(os.path.join(directory, item))
			and item.endswith(extensions)):
				yield os.path.splitext(item)[0], load_image(directory, item)
				
def slice_sprite_sheet(image, sub_image_size):
	image_width, image_height = image.get_width(), image.get_height()
	if (image_width % sub_image_size[0] != 0
		or image_height % sub_image_size[1] != 0):
			class NotEvenlyDivisable(Exception): pass
			raise NotEvenlyDivisable('Image width or height is not evenly divisable by sub image width or height.')
	images = []
	for index, x in enumerate(range(0, image_width, sub_image_size[0])):
		images.append([])
		for y in range(0, image_height, sub_image_size[1]):
				images[index].append(image.subsurface(pygame.Rect((x, y), sub_image_size)))
	return images
	
def blit_over(surface, rect, background):
	surface.blit(background.subsurface(rect), rect)
			
if __name__ == '__main_':
	pass