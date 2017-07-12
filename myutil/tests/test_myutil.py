import myutil
import pygame
import unittest
import os
import types
import itertools

#python -m unittest discover -t ..

def setUpModule():
	pygame.init()
	pygame.display.set_mode((1, 1))
	
def tearDownModule():
	pygame.quit()
	
class TestCC(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.x, cls.y, cls.cell_size = 2, 3, 32
		cls.coords = myutil.cc(cls.x, cls.y, cls.cell_size)

	def test_returns_tuple(self):
		self.assertIsInstance(self.coords, tuple)
		
	def test_returns_correct_coordinates(self):
		self.assertEqual(self.coords, (self.x*self.cell_size, self.y*self.cell_size))
	
class TestLoadImage(unittest.TestCase):
	
	@classmethod
	def setUpClass(cls):
		cls.image = myutil.load_image('images', 'test-image-1.png', (244, 244, 244))
		
	def test_is_surface(self):
		self.assertIsInstance(self.image, pygame.Surface)
		
	def test_surface_is_expected_size(self):
		self.assertEqual(self.image.get_size(), (32, 32))
		
	def test_surface_is_expected_color(self):
		self.assertEqual(self.image.get_at((0, 0)), (0, 0, 0))
		
	def test_surface_has_colorkey(self):
		self.assertEqual(self.image.get_colorkey(), (244, 244, 244, 255))
		
	def test_surface_has_no_colorkey(self):
		image = myutil.load_image('images', 'test-image-1.png')
		self.assertEqual(image.get_colorkey(), None)

class TestLoadImagesFromDirectory(unittest.TestCase):
		
	def test_is_generator(self):
		image_dict = myutil.load_images_from_directory('images', ()) ###image_dict bad name for this line (bad name completely)?
		self.assertIsInstance(image_dict, types.GeneratorType)

	def test_creates_dictionary(self): ###is this necessary?
		image_dict = dict(myutil.load_images_from_directory('images', ()))
		self.assertIsInstance(image_dict, dict)
		
	def test_returns_empty_dictionary(self):
		image_dict = dict(myutil.load_images_from_directory('images', ()))
		self.assertEqual(len(image_dict), 0)
		
	def test_loads_png(self):
		image_dict = dict(myutil.load_images_from_directory('images', ('png')))
		self.assertIsInstance(image_dict['test-image-1'], pygame.Surface)
		self.assertIsInstance(image_dict['test-image-2'], pygame.Surface)
		self.assertIsInstance(image_dict['test-sprite-sheet'], pygame.Surface)
		self.assertRaises(KeyError, lambda: image_dict['test-image-3'])
		self.assertRaises(KeyError, lambda: image_dict['test-image-4'])
		self.assertRaises(KeyError, lambda: image_dict['test-image-5'])
		self.assertRaises(KeyError, lambda: image_dict['test-image-6'])
			
	def test_loads_png_jpg(self):
		image_dict = dict(myutil.load_images_from_directory('images', ('png', 'jpg')))
		self.assertIsInstance(image_dict['test-image-1'], pygame.Surface)
		self.assertIsInstance(image_dict['test-image-2'], pygame.Surface)
		self.assertIsInstance(image_dict['test-image-3'], pygame.Surface)
		self.assertIsInstance(image_dict['test-image-4'], pygame.Surface)
		self.assertIsInstance(image_dict['test-sprite-sheet'], pygame.Surface)
		self.assertRaises(KeyError, lambda: image_dict['test-image-5'])
		self.assertRaises(KeyError, lambda: image_dict['test-image-6'])
		
	def test_loads_png_jpg_gif(self):
		image_dict = dict(myutil.load_images_from_directory('images', ('png', 'jpg', 'gif')))
		self.assertIsInstance(image_dict['test-image-1'], pygame.Surface)
		self.assertIsInstance(image_dict['test-image-2'], pygame.Surface)
		self.assertIsInstance(image_dict['test-image-3'], pygame.Surface)
		self.assertIsInstance(image_dict['test-image-4'], pygame.Surface)
		self.assertIsInstance(image_dict['test-image-5'], pygame.Surface)
		self.assertIsInstance(image_dict['test-image-6'], pygame.Surface)
		self.assertIsInstance(image_dict['test-sprite-sheet'], pygame.Surface)
		
class TestSliceSpriteSheet(unittest.TestCase):
	
	@classmethod
	def setUpClass(cls):
		cls.image = myutil.load_image('images', 'test-sprite-sheet.png')
		cls.sub_image_size = (32, 32)
		cls.image_list = myutil.slice_sprite_sheet(cls.image, cls.sub_image_size)
	
	def test_is_list(self):
		self.assertIsInstance(self.image_list, list)
		
	def test_list_contains_lists(self):
		for item in self.image_list:
			self.assertIsInstance(item, list)
			
	def test_lists_containing_lists_contains_surfaces(self):
		for list_ in self.image_list:
			for item in list_:
				self.assertIsInstance(item, pygame.Surface)
		
	def test_image_width_height_is_divided_evenly_by_sub_image_width_height(self):
		self.assertEqual(self.image.get_width()%self.sub_image_size[0], 0)
		self.assertEqual(self.image.get_height()%self.sub_image_size[1], 0)
	
	def test_is_correct_number_of_sub_images(self):
		self.assertEqual(len(self.image_list), self.image.get_width()/self.sub_image_size[0])
		for list_ in self.image_list:
			self.assertEqual(len(list_), self.image.get_height()/self.sub_image_size[1])
			
	def test_raises_exception_when_image_width_height_is_not_divided_evenly_by_sub_image_width_height(self):
		with self.assertRaises(Exception) as e: 
			myutil.slice_sprite_sheet(self.image, (23, 23))
		self.assertEqual('Image width or height is not evenly divisable by sub image width or height.', str(e.exception))
		
#class TestSurfaceCleaner(unittest.TestCase):
#	
#	@classmethod
#	def setUpClass(cls):
#		cls.surface_cleaner = myutil.SurfaceCleaner(pygame.Surface((1, 1)))
#		cls.dirty_rects = [pygame.Rect((1, 1), (1, 1)), pygame.Rect((1, 1), (1, 1)), pygame.Rect((1, 1), (1, 1))]
#	
#	def setUp(self):
#		self.surface_cleaner.dirty_rects = []
#		self.surface_cleaner.rects_and_backgrounds = []
#		
#	def test_dirty_rects_contains_one_empty_list_after_queuing_multiple_empty_lists(self):
#		self.surface_cleaner.queue_for_cleaning([])
#		self.surface_cleaner.queue_for_cleaning([])
#		self.assertEqual(len(self.surface_cleaner.dirty_rects), 1)
#		self.assertIsInstance(self.surface_cleaner.dirty_rects[0], list)
#	
#	def test_dirty_rects_contains_one_list_after_queuing(self):
#		self.surface_cleaner.queue_for_cleaning(dirty_rects=self.dirty_rects)
#		self.assertEqual(len(self.surface_cleaner.dirty_rects), 1)
#		self.surface_cleaner.queue_for_cleaning(dirty_rects=self.dirty_rects)
#		self.assertEqual(len(self.surface_cleaner.dirty_rects), 1)
#		
#	def test_dirty_rects_contains_three_lists_after_queuing_with_multiple_frames(self):
#		self.surface_cleaner.queue_for_cleaning(dirty_rects=self.dirty_rects, number_of_frames=3)
#		self.assertEqual(len(self.surface_cleaner.dirty_rects), 3)
#		self.surface_cleaner.queue_for_cleaning(dirty_rects=self.dirty_rects, number_of_frames=3)
#		self.assertEqual(len(self.surface_cleaner.dirty_rects), 3)
#		
#	def test_dirty_rects_contains_five_lists_after_queuing_with_multiple_frames_and_gaps(self):
#		self.surface_cleaner.queue_for_cleaning(dirty_rects=self.dirty_rects, number_of_frames=3, gap_between_each_frame=1)
#		self.assertEqual(len(self.surface_cleaner.dirty_rects), 5)
#		self.surface_cleaner.queue_for_cleaning(dirty_rects=self.dirty_rects, number_of_frames=3, gap_between_each_frame=1)
#		self.assertEqual(len(self.surface_cleaner.dirty_rects), 5)
#		
#	def test_dirty_rects_contains_nine_lists_after_queuing_with_multiple_frames_and_gaps(self):
#		self.surface_cleaner.queue_for_cleaning(dirty_rects=self.dirty_rects, number_of_frames=3, gap_between_each_frame=3)
#		self.assertEqual(len(self.surface_cleaner.dirty_rects), 9)
#		self.surface_cleaner.queue_for_cleaning(dirty_rects=self.dirty_rects, number_of_frames=3, gap_between_each_frame=3)
#		self.assertEqual(len(self.surface_cleaner.dirty_rects), 9)
#		
#	def test_clean_frame_removes_one_list_from_dirty_rects(self):
#		self.surface_cleaner.queue_for_cleaning(dirty_rects=self.dirty_rects, number_of_frames=3)
#		self.surface_cleaner.clean_frame()
#		self.assertEqual(len(self.surface_cleaner.dirty_rects), 2)
#		self.surface_cleaner.clean_frame()
#		self.assertEqual(len(self.surface_cleaner.dirty_rects), 1)
#		self.surface_cleaner.clean_frame()
#		self.assertEqual(len(self.surface_cleaner.dirty_rects), 0)
#		
#	def test_clean_frame_removes_first_list_from_dirty_rects(self):
#		self.surface_cleaner.queue_for_cleaning(dirty_rects=self.dirty_rects, number_of_frames=3)
#		first_item = self.surface_cleaner.dirty_rects[0]
#		self.surface_cleaner.clean_frame()
#		self.assertNotEqual(id(self.surface_cleaner.dirty_rects[0]), id(first_item))
		
if __name__ == '__main__':
	unittest.main()