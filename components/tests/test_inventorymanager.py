import components
import gameobjects
import myutil
import pygame
import unittest
import itertools

#python -m unittest discover -t ..

#Things to do:
#1. Refactor.

class TestInventoryManager(unittest.TestCase):
	
	@classmethod
	def setUpClass(cls):
		item_locations = [
			(0, 0), (32, 0), (64, 0), (96, 0),
			(0, 32), (32, 32), (32, 64), (32, 96)
		]
		equipped_item_location = (128, 0)
		cls.sprites = [ ###
			{'key': 'test', 'sprites': [None], 'max_count': 0},
		]
		cls.inventory = gameobjects.Inventory(
			(0, 0),
			(0, 0),
			'test-inventory',
			item_locations,
			equipped_item_location,
			None, 
			None,
			None, 
			cls.sprites,
			'test'
		)
		
	def setUp(self):
		self.inventory.inventory_manager.items = []
		self.inventory.inventory_manager.equipped_item = None
	
	def test_add_item_not_in_inventory(self):
		item = gameobjects.Item((0, 0), (0, 0), 'test-item', 1, True, None, self.sprites, 'test')
		self.inventory.inventory_manager.add_item(item)
		self.assertIn(item, self.inventory.inventory_manager.items)
		self.assertEqual(len(self.inventory.inventory_manager.items), 1)
		
	def test_add_item_already_in_inventory(self):
		item_1 = gameobjects.Item((0, 0), (0, 0), 'test-item', 1, True, None, self.sprites, 'test')
		item_2 = gameobjects.Item((0, 0), (0, 0), 'test-item', 1, True, None, self.sprites, 'test')
		self.inventory.inventory_manager.add_item(item_1)
		self.inventory.inventory_manager.add_item(item_2)
		self.assertIn(item_1, self.inventory.inventory_manager.items)
		self.assertNotIn(item_2, self.inventory.inventory_manager.items)
		self.assertEqual(len(self.inventory.inventory_manager.items), 1)
		self.assertEqual(self.inventory.inventory_manager.items[0].quantity, 2)
		
	def test_add_more_items_than_limit(self):
		for i in range(8):
			self.inventory.inventory_manager.add_item(
				gameobjects.Item((0, 0), (0, 0), 'test-item-{}'.format(i), 1, True, None, self.sprites, 'test')
			)
		item_9 = gameobjects.Item((0, 0), (0, 0), 'test-item-9', 1, True, None, self.sprites, 'test')
		self.inventory.inventory_manager.add_item(item_9)
		self.assertNotIn(item_9, self.inventory.inventory_manager.items)
		self.assertEqual(len(self.inventory.inventory_manager.items), 8)
		
	def test_added_items_are_in_proper_locations(self):
		for i in range(8):
			self.inventory.inventory_manager.add_item(
				gameobjects.Item((0, 0), (0, 0), 'test-item-{}'.format(i), 1, True, None, self.sprites, 'test')
			)
		self.inventory.inventory_manager.update_item_locations()
		for item, location in zip(self.inventory.inventory_manager.items, self.inventory.inventory_manager.item_locations):
			self.assertEqual(
				item.rect.topleft,
				(
					self.inventory.rect.x + location[0], 
					self.inventory.rect.y + location[1]
				)
			)
			
	def test_dropped_item_is_removed_from_inventory(self):
		item = gameobjects.Item((0, 0), (0, 0), 'test-item', 1, True, None, self.sprites, 'test')
		self.inventory.inventory_manager.add_item(item)
		self.inventory.inventory_manager.drop_item_at_location(item, (0, 0))
		self.assertNotIn(item, self.inventory.inventory_manager.items)
		
	def test_dropped_item_is_returned(self):
		item = gameobjects.Item((0, 0), (0, 0), 'test-item', 1, True, None, self.sprites, 'test')
		self.inventory.inventory_manager.add_item(item)
		i = self.inventory.inventory_manager.drop_item_at_location(item, (0, 0))
		self.assertIs(item, i)
		
	def test_dropped_item_is_in_proper_location(self):
		drop_location = (64, 64)
		item = gameobjects.Item((0, 0), (0, 0), 'test-item', 1, True, None, self.sprites, 'test')
		self.inventory.inventory_manager.add_item(item)
		self.inventory.inventory_manager.drop_item_at_location(item, drop_location)
		self.assertEqual(item.rect.topleft, drop_location)
	
	def test_dropping_item_not_in_inventory_has_no_effect(self):
		drop_location = (64, 64)
		item_1 = gameobjects.Item((0, 0), (0, 0), 'test-item-1', 1, True, None, self.sprites, 'test')
		item_2 = gameobjects.Item((0, 0), (0, 0), 'test-item-2', 1, True, None, self.sprites, 'test')
		self.inventory.inventory_manager.add_item(item_1)
		i = self.inventory.inventory_manager.drop_item_at_location(item_2, drop_location)
		self.assertEqual(self.inventory.inventory_manager.items, self.inventory.inventory_manager.items)
		self.assertIs(i, None)
	
	def test_item_becomes_equipped(self):
		item = gameobjects.Item((0, 0), (0, 0), 'test-item', 1, True, None, self.sprites, 'test')
		self.inventory.inventory_manager.add_item(item)
		self.assertIsNot(item, self.inventory.inventory_manager.equipped_item)
		self.inventory.inventory_manager.equip_item(item)
		self.assertIs(item, self.inventory.inventory_manager.equipped_item)
		
	def test_equipped_item_is_removed_from_items(self):
		item = gameobjects.Item((0, 0), (0, 0), 'test-item', 1, True, None, self.sprites, 'test')
		self.inventory.inventory_manager.add_item(item)
		self.inventory.inventory_manager.equip_item(item)
		self.assertNotIn(item, self.inventory.inventory_manager.items)
		
	def test_item_does_not_become_equipped_when_another_item_is_equipped(self):
		item_1 = gameobjects.Item((0, 0), (0, 0), 'test-item-1', 1, True, None, self.sprites, 'test')
		item_2 = gameobjects.Item((0, 0), (0, 0), 'test-item-2', 1, True, None, self.sprites, 'test')
		self.inventory.inventory_manager.add_item(item_1)
		self.inventory.inventory_manager.add_item(item_2)
		self.inventory.inventory_manager.equip_item(item_1)
		self.inventory.inventory_manager.equip_item(item_2)
		self.assertIsNot(item_2, self.inventory.inventory_manager.equipped_item)
	
	def test_item_only_equips_if_it_is_equippable(self):
		item = gameobjects.Item((0, 0), (0, 0), 'test-item', 1, False, None, self.sprites, 'test')
		self.inventory.inventory_manager.add_item(item)
		self.inventory.inventory_manager.equip_item(item)
		self.assertIn(item, self.inventory.inventory_manager.items)
		self.assertIsNot(item, self.inventory.inventory_manager.equipped_item)
	
	def test_equipped_item_is_in_proper_location(self):
		item = gameobjects.Item((0, 0), (0, 0), 'test-item', 1, True, None, self.sprites, 'test')
		self.inventory.inventory_manager.add_item(item)
		self.inventory.inventory_manager.equip_item(item)
		self.inventory.inventory_manager.update_item_locations()
		self.assertEqual(item.rect.topleft, self.inventory.inventory_manager.equipped_item_location)
		
	def test_unequip_item(self):
		item = gameobjects.Item((0, 0), (0, 0), 'test-item', 1, True, None, self.sprites, 'test')
		self.inventory.inventory_manager.add_item(item)
		self.inventory.inventory_manager.equip_item(item)
		self.inventory.inventory_manager.unequip_item(item)
		self.assertIn(item, self.inventory.inventory_manager.items)
		self.assertIs(self.inventory.inventory_manager.equipped_item, None)
		
	def test_cannot_unequip_item_if_inventory_is_full(self):
		item = gameobjects.Item((0, 0), (0, 0), 'test-item', 1, True, None, self.sprites, 'test')
		self.inventory.inventory_manager.add_item(item)
		self.inventory.inventory_manager.equip_item(item)
		for i in range(8):
			self.inventory.inventory_manager.add_item(
				gameobjects.Item((0, 0), (0, 0), 'test-item-{}'.format(i), 1, True, None, self.sprites, 'test')
			)
		self.inventory.inventory_manager.unequip_item(item)
		self.assertNotIn(item, self.inventory.inventory_manager.items)
		self.assertIs(self.inventory.inventory_manager.equipped_item, item)
		
	def test_cannot_unequip_item_that_is_not_equipped(self):
		item_1 = gameobjects.Item((0, 0), (0, 0), 'test-item-1', 1, True, None, self.sprites, 'test')
		item_2 = gameobjects.Item((0, 0), (0, 0), 'test-item-2', 1, True, None, self.sprites, 'test')
		self.inventory.inventory_manager.add_item(item_1)
		self.inventory.inventory_manager.add_item(item_2)
		self.inventory.inventory_manager.equip_item(item_1)
		self.inventory.inventory_manager.unequip_item(item_2)
		self.assertIs(self.inventory.inventory_manager.equipped_item, item_1)
		self.assertIn(item_2, self.inventory.inventory_manager.items)
		self.assertEqual(len(self.inventory.inventory_manager.items), 1)
		
	def test_items_with_quantity_zero_are_removed_from_inventory(self):
		item_1 = gameobjects.Item((0, 0), (0, 0), 'test-item-1', 1, True, None, self.sprites, 'test')
		item_2 = gameobjects.Item((0, 0), (0, 0), 'test-item-2', 1, True, None, self.sprites, 'test')
		self.inventory.inventory_manager.add_item(item_1)
		self.inventory.inventory_manager.add_item(item_2)
		item_2.quantity = 0
		self.inventory.inventory_manager.remove_spent_items()
		self.assertIn(item_1, self.inventory.inventory_manager.items)
		self.assertNotIn(item_2, self.inventory.inventory_manager.items)
		
	def test_full_returns_true_when_inventory_is_full(self):
		for i in range(self.inventory.inventory_manager.item_limit):
			self.inventory.inventory_manager.add_item(
				gameobjects.Item((0, 0), (0, 0), 'test-item-{}'.format(i), 1, True, None, self.sprites, 'test')
			)
		self.assertTrue(self.inventory.inventory_manager.is_full())
		
	def test_full_returns_false_when_inventory_is_not_full(self):
		for i in range(self.inventory.inventory_manager.item_limit-1):
			self.inventory.inventory_manager.add_item(
				gameobjects.Item((0, 0), (0, 0), 'test-item-{}'.format(i), 1, True, None, self.sprites, 'test')
			)
		self.assertFalse(self.inventory.inventory_manager.is_full())