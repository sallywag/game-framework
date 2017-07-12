import components
import gameobjects
import myutil
import pygame
import unittest

#python -m unittest discover -t ..

class TestSurfaceCleaner(unittest.TestCase):
	
	@classmethod
	def setUpClass(cls):
		pygame.init()
		displaysurf = pygame.display.set_mode((1, 1))
		background = myutil.load_image('images', 'background.png')
		cls.surface_cleaner = myutil.SurfaceCleaner(displaysurf, background)
		cls.gameobject = gameobjects.GameObject((0, 0), (1, 1), 'test')
		cls.test_sprite_sheet = myutil.load_image('images', 'test-sprite-sheet.png')
		cls.test_sprite_sheet = myutil.slice_sprite_sheet(cls.test_sprite_sheet, (32, 32))
		sprites = [
			{
				'key': 'test', 
				'sprites': [cls.test_sprite_sheet[0][0], cls.test_sprite_sheet[1][0], cls.test_sprite_sheet[2][0]], 
				'max_count': 0
			}
		]
		cls.gameobject.sprite_manager = components.SpriteManager(sprites, 'test')
		cls.gameobject.sprite_manager.get_next_sprite() #First sprite...
		cls.container = [cls.gameobject]
		cls.surface_cleaner.add([[cls.gameobject]], [cls.container])
	
	@classmethod
	def tearDownClass(cls):
		pygame.quit()
	
	def test_adding_gameobject_adds_single_item_to_empty_relevant_data_dict(self):
		self.assertEqual(len(self.surface_cleaner.relevant_data), 1)
		
	def test_added_item_uses_gameobject_as_key(self):
		for key in self.surface_cleaner.relevant_data.keys():
			self.assertIs(key, self.gameobject)
			
	def test_added_item_is_dict(self):
		self.assertIsInstance(self.surface_cleaner.relevant_data[self.gameobject], dict)
			
	def test_added_item_is_expected_size(self):
		self.assertEqual(len(self.surface_cleaner.relevant_data[self.gameobject]), 3)
			
	def test_added_item_has_expected_key_names(self):
		self.assertEqual(
			sorted(self.surface_cleaner.relevant_data[self.gameobject].keys()), 
			['container', 'location', 'sprite']
		)
		
	def test_added_item_contains_gameobjects_current_container_location_and_sprite(self):
		self.assertIs(self.surface_cleaner.relevant_data[self.gameobject]['container'], self.container)
		self.assertEqual(
			self.surface_cleaner.relevant_data[self.gameobject]['location'], 
			self.gameobject.rect.topleft
		)
		self.assertIs(
			self.surface_cleaner.relevant_data[self.gameobject]['sprite'], 
			self.gameobject.sprite_manager.current_sprite
		)
		
	def test_moving_gameobject_updates_location_in_relevant_data_dict_with_gameobjects_location(self):
		self.gameobject.rect.topleft = (
			self.gameobject.rect.x + 32, 
			self.gameobject.rect.y + 32
		)
		self.surface_cleaner._update_relevant_data(self.gameobject)
		self.assertEqual(
			self.surface_cleaner.relevant_data[self.gameobject]['location'], 
			self.gameobject.rect.topleft
		)
		
	def test_changing_gameobjects_sprite_updates_sprite_in_relevant_data_dict(self):
		self.gameobject.sprite_manager.get_next_sprite()
		self.surface_cleaner._update_relevant_data(self.gameobject)
		self.assertIs(
			self.surface_cleaner.relevant_data[self.gameobject]['sprite'], 
			self.gameobject.sprite_manager.current_sprite
		)
		
	def test_moving_gameobject_adds_two_rects_to_dirty_rects(self): ###
		self.assertEqual(len(self.surface_cleaner.dirty_rects), 0)
		self.gameobject.rect.topleft = (
			self.gameobject.rect.x + 32, 
			self.gameobject.rect.y + 32
		)
		self.surface_cleaner._blit_over_gameobjects_previous_location(self.gameobject)
		self.assertEqual(len(self.surface_cleaner.dirty_rects), 2)
		self.surface_cleaner.dirty_rects = []
		
	def test_moving_gameobject_adds_expected_rects_to_dirty_rects(self):
		previous_location = self.gameobject.rect.topleft
		self.gameobject.rect.topleft = (
			self.gameobject.rect.x + 32, 
			self.gameobject.rect.y + 32
		)
		self.surface_cleaner._blit_over_gameobjects_previous_location(self.gameobject)
		self.assertEqual(
			{rect.topleft for rect in self.surface_cleaner.dirty_rects}, 
			{
				previous_location,
				self.gameobject.rect.topleft
			}
		)
		self.surface_cleaner.dirty_rects = []
		
	def test_changing_gameobjects_sprite_adds_rect_to_dirty_rects(self): 
		self.assertEqual(len(self.surface_cleaner.dirty_rects), 0)
		self.gameobject.sprite_manager.get_next_sprite()
		self.surface_cleaner._blit_over_gameobject(self.gameobject)
		self.assertEqual(len(self.surface_cleaner.dirty_rects), 1)
		self.surface_cleaner.dirty_rects = []
		
	def test_changing_gameobjects_sprite_adds_expected_rect_to_dirty_rects(self):
		self.gameobject.sprite_manager.get_next_sprite()
		self.surface_cleaner._blit_over_gameobject(self.gameobject)
		self.assertEqual(
			self.surface_cleaner.dirty_rects[0].topleft, 
			self.gameobject.rect.topleft
		)
		self.surface_cleaner.dirty_rects = []
	
	def test_removing_gameobject_from_container_adds_rect_to_dirty_rects(self): 
		self.assertEqual(len(self.surface_cleaner.dirty_rects), 0)
		self.container.remove(self.gameobject)
		self.surface_cleaner._blit_over_gameobject(self.gameobject)
		self.assertEqual(len(self.surface_cleaner.dirty_rects), 1)
		self.surface_cleaner.dirty_rects = []
		self.container.append(self.gameobject)
		
	def test_removing_gameobject_from_container_adds_expeced_rect_to_dirty_rects(self):
		self.container.remove(self.gameobject)
		self.surface_cleaner._blit_over_gameobject(self.gameobject)
		self.assertEqual(
			self.surface_cleaner.dirty_rects[0].topleft, 
			self.gameobject.rect.topleft
		)
		self.surface_cleaner.dirty_rects = []
		self.container.append(self.gameobject)