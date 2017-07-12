import components
import gameobjects
import myutil
import pygame
import unittest

#python -m unittest discover -t ..

def setUpModule():
	pygame.init()

def tearDownModule():
	pygame.quit()

class TestSurfaceCleaner(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.displaysurf = pygame.display.set_mode((1, 1))
		cls.image = myutil.load_image('images', 'background.png')
		cls.gameobject = gameobjects.GameObject((0, 0), (1, 1), 'test')
		test_sprite_sheet = myutil.load_image('images', 'test-sprite-sheet.png')
		test_sprite_sheet = myutil.slice_sprite_sheet(test_sprite_sheet, (32, 32))
		sprites = [{'key': 'test', 'sprites': [test_sprite_sheet[0][0], test_sprite_sheet[1][0], test_sprite_sheet[2][0]], 'max_count': 0}]
		cls.gameobject.sprite_manager = components.SpriteManager(sprites, 'test')
		cls.container = [cls.gameobject]
		cls.gameobject.surface_cleaner = components.SurfaceCleaner(cls.gameobject, cls.container)
	
	def setUp(self):
		components.SurfaceCleaner.dirty_rects = []

	def test_queue_for_cleaning_gameobject_moved(self):
		self.gameobject.rect.topleft = (2, 2)
		self.gameobject.surface_cleaner.queue_for_cleaning(self.displaysurf, self.image)
		self.assertEqual(len(components.SurfaceCleaner.dirty_rects), 2)

	def test_queue_for_cleaning_sprite_changed(self):
		self.gameobject.sprite_manager.get_next_sprite()
		self.gameobject.sprite_manager.get_next_sprite()
		self.gameobject.surface_cleaner.queue_for_cleaning(self.displaysurf, self.image)
		self.assertEqual(len(components.SurfaceCleaner.dirty_rects), 1)

	def test_queue_for_cleaning_removed_from_container(self):
		self.container.remove(self.gameobject)
		self.gameobject.surface_cleaner.queue_for_cleaning(self.displaysurf, self.image)
		self.assertEqual(len(components.SurfaceCleaner.dirty_rects), 1)

	def test_clean(self):
		self.gameobject.rect.topleft = (4, 4)
		self.gameobject.surface_cleaner.queue_for_cleaning(self.displaysurf, self.image)
		components.SurfaceCleaner.clean(self.displaysurf)
		self.assertEqual(len(components.SurfaceCleaner.dirty_rects), 0)