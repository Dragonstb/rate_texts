import unittest
import sys
sys.path.append('..')
sys.path.append('../..')
sys.path.append('../../rate_texts')
# autopep8: off
from rate_texts.dev_tools.story_teller.region_node import RegionNode
# autopep8: on

_PLACES = 'places'

class TestRegionNode(unittest.TestCase):

    def test_constructor(self):
        name = 'Sam'
        tags = ['cool', 'intelligent']
        variants = ['Samantha', 'Samuel']

        node = RegionNode(name, variants, tags)
        self.assertIsNotNone( node.tags, 'No tags in node.')
        self.assertEqual( len(tags), len(node.tags), 'Wrong number of tags.')
        for tag in tags:
            self.assertTrue( tag in node.tags, f'Missing tag {tag}.' )
        self.assertEqual( len(variants), len(node.variants[_PLACES]), 'Wrong number of places.')
        for var in variants:
            self.assertTrue( var in node.variants[_PLACES], f'Missing place {var}.' )
        
    def test_name_default(self):
        name = 'Sam'
        node = RegionNode(name)
        self.assertEqual(name, node.get_name(), 'Wrong name')

    def test_name_place(self):
        name = 'Sam'
        places = ['left','right']
        node = RegionNode(name, places=places)
        place = node.get_name(_PLACES)
        self.assertTrue( place in node.variants[_PLACES], 'Wrong place')


if __name__ == '__main__':
    unittest.main()