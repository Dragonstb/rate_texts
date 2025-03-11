import unittest
import sys
import copy
sys.path.append('..')
sys.path.append('../..')
sys.path.append('../../rate_texts')
# autopep8: off
from rate_texts.dev_tools.story_teller.entity_node import EntityNode
from rate_texts.dev_tools.story_teller.entity_factory import EntityFactory
from rate_texts.dev_tools.story_teller.story_element_node import StoryElementNode
from rate_texts.dev_tools.story_teller.story_element_resolver import StoryElementResolver
from rate_texts.dev_tools.story_teller.story_element_almanach import StoryElementAlmanach
from rate_texts.dev_tools.story_teller.placeholder_resolver import PlaceholderResolver
# autopep8: on

_NAME = 'Sam'

class HelpStrategy(StoryElementResolver):

    def resolve_element(self, typ, tag):
        return EntityNode(_NAME, [tag])


class TestPlaceholderResolver(unittest.TestCase):

    def test_register_strategy(self):
        strategy = HelpStrategy(StoryElementAlmanach(EntityFactory(['doesntmatter'])))
        res = PlaceholderResolver()
        res.set_strategy_for(_NAME, strategy)

        self.assertTrue( _NAME in res.strategies.keys(), 'Key not registered')
        self.assertEqual( strategy, res.strategies[_NAME], 'Strategy not registered')

    def test_resolve(self):
        strategy = HelpStrategy(StoryElementAlmanach(EntityFactory(['doesntmatter'])))
        res = PlaceholderResolver()
        res.set_strategy_for(_NAME, strategy)

        node = res.resolve(_NAME, 'typ', 'tag')

        self.assertIsNotNone( node, 'No node at all')
        self.assertEqual( _NAME, node.get_name(), 'Wrong name')