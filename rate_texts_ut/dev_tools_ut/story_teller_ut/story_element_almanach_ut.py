import unittest
import sys
import copy
sys.path.append('..')
sys.path.append('../..')
sys.path.append('../../rate_texts')
# autopep8: off
from rate_texts.dev_tools.story_teller.entity_node import EntityNode
from rate_texts.dev_tools.story_teller.entity_factory import EntityFactory
from rate_texts.dev_tools.story_teller.story_element_almanach import StoryElementAlmanach
# autopep8: on

class TestStoryElementAlmanach(unittest.TestCase):

    def test_create(self):
        name = 'Sam'
        names = [name]
        factory = EntityFactory(names)
        al = StoryElementAlmanach(factory)
        tag = 'funky'

        ini_length = al.count_elements()
        node = al.create_element(tag)
        final_length = al.count_elements()

        self.assertEqual(0, ini_length, 'Wrong initial number of elements')
        self.assertEqual(1, final_length, 'Wrong final number of elements')
        self.assertEqual(name, node.get_name(), 'Wrong name')
        self.assertTrue( node in al.elements[tag], 'Node not registered')

    def test_get_or_create_nonexisting(self):
        name = 'Sam'
        names = [name]
        factory = EntityFactory(names)
        al = StoryElementAlmanach(factory)
        tag = 'funky'

        ini_length = al.count_elements()
        node = al.get_or_create_element(tag)
        final_length = al.count_elements()

        self.assertEqual(0, ini_length, 'Wrong initial number of elements')
        self.assertEqual(1, final_length, 'Wrong final number of elements')
        self.assertEqual(name, node.get_name(), 'Wrong name')
        self.assertTrue( node in al.elements[tag], 'Node not registered')

    def test_get_or_create_existing(self):
        name = 'Sam'
        names = [name]
        factory = EntityFactory(names)
        al = StoryElementAlmanach(factory)
        tag = 'funky'

        node = al.create_element(tag)

        ini_length = al.count_elements()
        node = al.get_or_create_element(tag)
        final_length = al.count_elements()

        self.assertEqual(1, ini_length, 'Wrong initial number of elements')
        self.assertEqual(1, final_length, 'Wrong final number of elements')
        self.assertEqual(name, node.get_name(), 'Wrong name')
        self.assertTrue( node in al.elements[tag], 'Node not registered')