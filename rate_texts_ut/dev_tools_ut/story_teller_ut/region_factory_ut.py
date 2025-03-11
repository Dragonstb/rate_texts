import unittest
import sys
import copy
from typing import DefaultDict, List, Dict
sys.path.append('..')
sys.path.append('../..')
sys.path.append('../../rate_texts')
# autopep8: off
from rate_texts.dev_tools.story_teller.region_node import RegionNode
from rate_texts.dev_tools.story_teller.region_factory import RegionFactory
# autopep8: on

_NAME = 'name'
_PLACES = 'places'

class TestRegionFactory(unittest.TestCase):

    def test_pick(self):
        regionA = DefaultDict()
        regionA[_NAME] = 'a'
        regionA[_PLACES] = ['near a']
        regions: List[DefaultDict|Dict] = [regionA]

        factory = RegionFactory(regions)
        region = factory._pick()

        self.assertEqual( regionA, region, 'Factory has incorrect number of available names left')        

    def test_make_new(self):
        regionA = DefaultDict()
        regionA[_NAME] = 'a'
        regionA[_PLACES] = ['near a']
        regions: List[DefaultDict|Dict] = [regionA]
        factory = RegionFactory(regions)
        tags = ['quaint', 'picturesque']

        node = factory.make_new(tags)

        self.assertIsNotNone( node, 'No node at all.')
        self.assertEqual( len(tags), len(node.tags), 'Wrong number of tags.')
        for tag in tags:
            self.assertTrue( tag in node.tags, f'Missing tag {tag}.' )
        self.assertEqual( regionA[_NAME], node.get_name(), 'Wrong name')


if __name__ == '__main__':
    unittest.main()