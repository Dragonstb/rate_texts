import unittest
import sys
sys.path.append('..')
sys.path.append('../..')
sys.path.append('../../rate_texts')
# autopep8: off
from rate_texts.dev_tools.story_teller.entity_node import EntityNode
# autopep8: on

_G = 'g'

class TestEntityNode(unittest.TestCase):

    def test_constructor(self):
        name = 'Sam'
        tags = ['cool', 'intelligent']

        node = EntityNode(name, tags)
        self.assertIsNotNone( node.tags, 'No tags in node.')
        self.assertEqual( len(tags), len(node.tags), 'Wrong number of tags.')
        for tag in tags:
            self.assertTrue( tag in node.tags, f'Missing tag {tag}.' )
        
    def test_name_default(self):
        name = 'Sam'
        node = EntityNode(name)
        self.assertEqual(name, node.get_name(), 'Wrong name')

    def test_name_genitive_with_s(self):
        name = 'Sam'
        node = EntityNode(name)
        self.assertEqual(name+"'s", node.get_name(_G), 'Wrong name')

    def test_name_genitive_without_s_on_x(self):
        name = 'Alex'
        node = EntityNode(name)
        self.assertEqual(name+"'", node.get_name(_G), 'Wrong name')

    def test_name_genitive_without_s_on_s(self):
        name = 'Mnclahchhdjs'
        node = EntityNode(name)
        self.assertEqual(name+"'", node.get_name(_G), 'Wrong name')

    def test_name_genitive_without_s_on_th(self):
        name = 'Kbfvskjvckth'
        node = EntityNode(name)
        self.assertEqual(name+"'", node.get_name(_G), 'Wrong name')



if __name__ == '__main__':
    unittest.main()