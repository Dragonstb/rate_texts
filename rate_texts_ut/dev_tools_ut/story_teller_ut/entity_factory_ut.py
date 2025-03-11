import unittest
import sys
import copy
sys.path.append('..')
sys.path.append('../..')
sys.path.append('../../rate_texts')
# autopep8: off
from rate_texts.dev_tools.story_teller.entity_node import EntityNode
from rate_texts.dev_tools.story_teller.entity_factory import EntityFactory
# autopep8: on

class TestEntityFactory(unittest.TestCase):

    def test_extract_from_pool_one(self):
        names = ['Sam', 'Alex']
        factory = EntityFactory(copy.copy(names))
        name = factory._extract_from_pool()

        self.assertTrue( name in names, f'Picked non existing name {name}')
        self.assertEqual( len(names)-1, len(factory.availible_names), 'Factory has incorrect number of available names left')
        self.assertEqual( 1, len(factory.depleted_names), 'Incorrect number of depleted names')

    def test_extract_from_pool_last(self):
        names = ['Sam', 'Alex']
        factory = EntityFactory(copy.copy(names))
        # pick all names
        for _ in range(len(names)):
            factory._extract_from_pool()
        self.assertEqual( 0, len(factory.availible_names), 'Incorrect number of available names left after picking all')
        self.assertEqual( len(names), len(factory.depleted_names), 'Incorrect number of depleted names after picking all')

        # pick a further name, which should restore the list of available names first
        name = factory._extract_from_pool()

        self.assertTrue( name in names, f'Picked non existing name {name}')
        self.assertEqual( len(names)-1, len(factory.availible_names), 'Factory has incorrect number of available names left')
        self.assertEqual( 1, len(factory.depleted_names), 'Incorrect number of depleted names')

    def test_make_new(self):
        name = 'Sam'
        names = [name]
        factory = EntityFactory(copy.copy(names))
        tags = ['cool', 'awesome']
        
        node = factory.make_new(tags)

        self.assertIsNotNone( node, 'No node at all.')
        self.assertEqual( len(tags), len(node.tags), 'Wrong number of tags.')
        for tag in tags:
            self.assertTrue( tag in node.tags, f'Missing tag {tag}.' )
        self.assertEqual( name, node.get_name(), 'Wrong name')
        self.assertEqual( len(names)-1, len(factory.availible_names), 'Factory has incorrect number of available names left')
        self.assertEqual( 1, len(factory.depleted_names), 'Incorrect number of depleted names')


if __name__ == '__main__':
    unittest.main()