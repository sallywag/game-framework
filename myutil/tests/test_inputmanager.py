import myutil
import pygame
import unittest

#python -m unittest discover -t ..

#1 - left click
#2 - middle click
#3 - right click
#4 - scroll up
#5 - scroll down

class TestInputManager(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		pygame.init() 
		displaysurf = pygame.display.set_mode((1, 1))
		cls.left_mouse_button = 1
		
	def tearDown(self):
		myutil.InputManager.keyboard.clear()
		myutil.InputManager.mouse.clear()
		
	def test_quit_flag_is_set_to_true_when_quit_event_is_in_event_queue(self):
		myutil.InputManager.get_events()
		myutil.InputManager.check_for_quit_event()
		self.assertFalse(myutil.InputManager.quit)
		pygame.event.post(pygame.event.Event(pygame.QUIT))
		myutil.InputManager.get_events()
		myutil.InputManager.check_for_quit_event()
		self.assertTrue(myutil.InputManager.quit)
		
	def test_space_bar_key_is_pressed(self):
		pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
		myutil.InputManager.get_events()
		myutil.InputManager.get_keyboard_input()
		self.assertEqual(myutil.InputManager.keyboard[pygame.K_SPACE], myutil.InputManager.pressed)
		
	def test_space_bar_key_is_held(self):
		pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
		myutil.InputManager.get_events()
		myutil.InputManager.get_keyboard_input()
		myutil.InputManager.update_keyboard_key_state()
		self.assertEqual(myutil.InputManager.keyboard[pygame.K_SPACE], myutil.InputManager.held)	
	
	def test_space_bar_key_is_released(self):
		pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_SPACE))
		myutil.InputManager.get_events()
		myutil.InputManager.get_keyboard_input()
		self.assertEqual(myutil.InputManager.keyboard[pygame.K_SPACE], myutil.InputManager.released)
		
	def test_released_space_bar_key_is_None(self):
		pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_SPACE))
		myutil.InputManager.get_events()
		myutil.InputManager.get_keyboard_input()
		myutil.InputManager.update_keyboard_key_state()
		self.assertIs(myutil.InputManager.keyboard[pygame.K_SPACE], None)

	def test_mouse_cursor_is_at_expected_location(self):
		expected_cursor_location = (32, 32)
		pygame.event.post(pygame.event.Event(pygame.MOUSEMOTION, pos=expected_cursor_location))
		myutil.InputManager.get_events()
		myutil.InputManager.get_mouse_input()
		self.assertEqual(myutil.InputManager.cursor_location, expected_cursor_location)
		
	def test_left_mouse_button_is_pressed(self):
		pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=self.left_mouse_button))
		myutil.InputManager.get_events()
		myutil.InputManager.get_mouse_input()
		self.assertEqual(myutil.InputManager.mouse[self.left_mouse_button], myutil.InputManager.pressed) 
		
	def test_left_mouse_button_key_is_held(self):
		pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=self.left_mouse_button))
		myutil.InputManager.get_events()
		myutil.InputManager.get_mouse_input()
		myutil.InputManager.update_mouse_button_state()
		self.assertEqual(myutil.InputManager.mouse[self.left_mouse_button], myutil.InputManager.held)	
		
	def test_left_mouse_button_is_released(self):
		pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, button=self.left_mouse_button))
		myutil.InputManager.get_events()
		myutil.InputManager.get_mouse_input()
		self.assertEqual(myutil.InputManager.mouse[self.left_mouse_button], myutil.InputManager.released)
		
	def test_left_mouse_button_is_None(self):
		pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, button=self.left_mouse_button))
		myutil.InputManager.get_events()
		myutil.InputManager.get_mouse_input()
		myutil.InputManager.update_mouse_button_state()
		self.assertIs(myutil.InputManager.mouse[self.left_mouse_button], None)