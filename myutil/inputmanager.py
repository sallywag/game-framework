import collections
import pygame


class InputManager:

	keyboard = collections.defaultdict(lambda: None)
	mouse = collections.defaultdict(lambda: None)
	cursor_location = None
	quit = False
	events = None
	pressed = 'pressed'
	held = 'held'
	released = 'released'
	
	@classmethod
	def get_events(cls):
		cls.events = pygame.event.get()
		
	@classmethod
	def check_for_quit_event(cls):
		for event in cls.events:
			if event.type == pygame.QUIT:
				cls.quit = True
				break
	
	@classmethod
	def update_keyboard_key_state(cls):
		for key, state in cls.keyboard.items():
			if state == cls.pressed:
				cls.keyboard[key] = cls.held
			elif state == cls.released:
				cls.keyboard[key] = None
				
	@classmethod
	def get_keyboard_input(cls):
		for event in cls.events:
			if event.type == pygame.KEYDOWN:
				if cls.keyboard[event.key] is None:
					cls.keyboard[event.key] = cls.pressed
			elif event.type == pygame.KEYUP:
				cls.keyboard[event.key] = cls.released
				
	@classmethod
	def update_mouse_button_state(cls):
		for button, state in cls.mouse.items():
			if state == cls.pressed:
				cls.mouse[button] = cls.held
			elif state == cls.released:
				cls.mouse[button] = None
		
	@classmethod
	def get_mouse_input(cls):
		for event in cls.events:
			if event.type == pygame.MOUSEMOTION:
				cls.cursor_location = event.pos
			if event.type == pygame.MOUSEBUTTONDOWN:
				if cls.mouse[event.button] is None:
					cls.mouse[event.button] = cls.pressed
			elif event.type == pygame.MOUSEBUTTONUP:
				cls.mouse[event.button] = cls.released