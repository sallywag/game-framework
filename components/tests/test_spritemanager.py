import components
import gameobjects
import myutil
import pygame
import unittest
import itertools

#python -m unittest discover -t ..

def setUpModule():
	pygame.init()
	pygame.display.set_mode((1, 1))
	
def tearDownModule():
	pygame.quit()

class TestSpriteGroup(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.image_dict = dict(myutil.load_images_from_directory('images', ('png')))
		cls.sprite_group = components.spritemanager.SpriteGroup(
			[
				cls.image_dict['test-up'],
				cls.image_dict['test-down'],
				cls.image_dict['test-left'],
				cls.image_dict['test-right']
			], 1
		)
		cls.sprite_group_size = len(cls.sprite_group.sprites)
		cls.expected_size = 4
	
	def test_contains_expected_number_of_items(self):
		self.assertEqual(self.sprite_group_size, self.expected_size)
		
	def test_contained_items_are_surfaces(self):
		for item in self.sprite_group.sprites:
			self.assertIsInstance(item, pygame.Surface)
			
	def test_sprites_attribute_is_cycle_generator(self):
		self.assertIsInstance(self.sprite_group.sprite_reel, itertools.cycle)
	
	def test_get_next_sprite_returns_surfaces(self):
		for i in range(len(self.sprite_group.sprites)):
			self.assertIsInstance(self.sprite_group.get_next_sprite(), pygame.Surface)
		
	def test_cycles_endlessly(self):
		for i in range(self.sprite_group_size+4):
			self.assertIsInstance(self.sprite_group.get_next_sprite(), pygame.Surface)
			
	def test_returnes_the_same_expected_sprites_over_and_over(self):
		set_ = set(id(self.sprite_group.get_next_sprite()) for i in range(self.sprite_group_size+8))
		self.assertEqual(len(set_), self.sprite_group_size)
		
	def test_returns_next_sprite_half_as_frequently(self): ###!!! 2 and 1 returns 2 sprites because len(sprite_group)
		sprite_group = components.spritemanager.SpriteGroup(
			[
				self.image_dict['test-up'],
				self.image_dict['test-down'],
				self.image_dict['test-left'],
				self.image_dict['test-right']
			], 1
		)
		number_of_sprites = len(set(sprite_group.get_next_sprite() for i in range(len(sprite_group.sprites))))
		self.assertEqual(number_of_sprites, 2)
		
	def test_sprite_group_properly_resets(self):
		sprite_group = components.spritemanager.SpriteGroup(
			[
				self.image_dict['test-up'],
				self.image_dict['test-down'],
				self.image_dict['test-left'],
				self.image_dict['test-right']
			], 0
		)
		first_sprite = sprite_group.sprites[0]
		for i in range(2):
			sprite_group.get_next_sprite()
		sprite_group.reset()
		self.assertEqual(first_sprite, sprite_group.current_sprite)
		self.assertEqual(sprite_group.current_count, sprite_group.max_count)
		
class TestSpriteManager(unittest.TestCase):
			
	def setUp(self):
		sprites = [
			{'key': 'test-1', 'sprites': ['sprite-1', 'sprite-2', 'sprite-3', 'sprite-4'], 'max_count': 0},
			{'key': 'test-2', 'sprites': ['sprite-a', 'sprite-b', 'sprite-c', 'sprite-d'], 'max_count': 1} ### SOURCE OF YOUR BUGS WERE NOT REALL BUGS MAX COUNT!!!!
		]
		self.gameobject = gameobjects.GameObject((1, 1), (1, 1), 'test-gameobject')
		self.gameobject.sprite_manager = components.SpriteManager(sprites, 'test-1')
	
	def test_sprites_contains_sprite_groups(self):
		for key, item in self.gameobject.sprite_manager.sprites.items():
			self.assertIsInstance(item, components.spritemanager.SpriteGroup)
			
	def test_get_next_sprite_with_empty_reel(self):
		self.assertEqual(self.gameobject.sprite_manager.get_next_sprite(), 'sprite-1')
		self.assertEqual(self.gameobject.sprite_manager.get_next_sprite(), 'sprite-2')
		
	def test_set_sprite_group(self):
		self.gameobject.sprite_manager.set_sprite_group('test-2')
		self.assertEqual(self.gameobject.sprite_manager.current_sprite_group, self.gameobject.sprite_manager.sprites['test-2'])
		
	def test_get_next_sprite_before_and_after_set_sprite_group(self):
		self.assertEqual(self.gameobject.sprite_manager.get_next_sprite(), 'sprite-1')
		self.assertEqual(self.gameobject.sprite_manager.get_next_sprite(), 'sprite-2')
		self.gameobject.sprite_manager.set_sprite_group('test-2')
		self.assertEqual(self.gameobject.sprite_manager.get_next_sprite(), 'sprite-a')
		self.assertEqual(self.gameobject.sprite_manager.get_next_sprite(), 'sprite-a')
		self.assertEqual(self.gameobject.sprite_manager.get_next_sprite(), 'sprite-b')
		self.assertEqual(self.gameobject.sprite_manager.get_next_sprite(), 'sprite-b')
		self.gameobject.sprite_manager.set_sprite_group('test-1')
		self.assertEqual(self.gameobject.sprite_manager.get_next_sprite(), 'sprite-1')
		self.assertEqual(self.gameobject.sprite_manager.get_next_sprite(), 'sprite-2')
	
	def test_add_to_reel(self):
		self.gameobject.sprite_manager.add_to_reel('test-2')
		expected_reel = ['sprite-a', 'sprite-a', 'sprite-b', 'sprite-b', 'sprite-c', 'sprite-c', 'sprite-d', 'sprite-d']
		self.assertEqual(self.gameobject.sprite_manager.reel, expected_reel)
		
	def test_get_next_sprite_with_reel(self):
		self.gameobject.sprite_manager.add_to_reel('test-2')
		self.assertEqual(self.gameobject.sprite_manager.get_next_sprite(), 'sprite-a')
		self.assertEqual(self.gameobject.sprite_manager.get_next_sprite(), 'sprite-a')
		self.assertEqual(self.gameobject.sprite_manager.get_next_sprite(), 'sprite-b')
		self.assertEqual(self.gameobject.sprite_manager.get_next_sprite(), 'sprite-b')
		self.assertEqual(self.gameobject.sprite_manager.get_next_sprite(), 'sprite-c')
		self.assertEqual(self.gameobject.sprite_manager.get_next_sprite(), 'sprite-c')
		self.assertEqual(self.gameobject.sprite_manager.get_next_sprite(), 'sprite-d')
		self.assertEqual(self.gameobject.sprite_manager.get_next_sprite(), 'sprite-d')
		self.assertEqual(self.gameobject.sprite_manager.get_next_sprite(), 'sprite-1')
		self.assertEqual(self.gameobject.sprite_manager.get_next_sprite(), 'sprite-2')