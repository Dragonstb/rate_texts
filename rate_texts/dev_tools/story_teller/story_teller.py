from typing import List, DefaultDict, Dict
from rate_texts.dev_tools.story_teller.story_element_almanach import StoryElementAlmanach
from rate_texts.dev_tools.story_teller.entity_node import EntityNode
from rate_texts.dev_tools.story_teller.entity_factory import EntityFactory
from rate_texts.dev_tools.story_teller.placeholder_resolver import PlaceholderResolver
from rate_texts.dev_tools.story_teller.story_element_resolver import StoryElementResolver
from rate_texts.dev_tools.story_teller.story_element_resolver import EntityResolverBuilder, RegionResolverBuilder
from rate_texts.dev_tools.story_teller.story_factory import StoryFactory
from rate_texts.dev_tools.story_teller.story_node import StoryNode
import re
from pathlib import Path
import json
import rate_texts.dev_tools.town_gen as town_gen
from typing import DefaultDict


class StoryTeller:

    resolver: PlaceholderResolver
    factory: StoryFactory

    def __init__(self, config: Dict | None = None) -> None:
        # load or set configuration
        if config is None:
            contents = dict()
            # may raise error
            path = Path(__file__).parent
            path = Path(path, 'stories.json')
            if path.exists() and path.is_file():
                with open(path, 'rt') as file:
                    contents = json.load(file)
        else:
            contents = config

        _REGIONS = 'regions'
        _NAMES = 'char_names'
        _NODES = 'story_nodes'

        # character names
        if _NAMES not in contents.keys():
            raise ValueError('Contents do not contains character names')
        names = contents[_NAMES]
        builder = EntityResolverBuilder(names)
        char_resolver = builder.build()

        # town names
        names = town_gen.gen_towns(30)
        builder = EntityResolverBuilder(names)
        town_resolver = builder.build()

        # regions
        if _REGIONS not in contents.keys():
            raise ValueError('Contents do not contains regions')
        region_resolver = RegionResolverBuilder(contents[_REGIONS]).build()

        # resolver
        self.resolver = PlaceholderResolver()
        self.resolver.set_strategy_for('c', char_resolver)
        self.resolver.set_strategy_for('t', town_resolver)
        self.resolver.set_strategy_for('r', region_resolver)

        # story fragments
        fragments = contents[_NODES]
        self.factory = StoryFactory(fragments)

    # ---------------------------------------------------------

    def tell_story(self) -> str:
        # TODO: reset almanachs, town name list and such
        lineage = []
        initial_node = self.factory.get_initial()
        if initial_node is None:
            raise RuntimeError('No initial nodes available.')

        for tag in initial_node.tags:
            if tag not in lineage:
                lineage.append(tag)

        nodes: List[StoryNode | None] = [initial_node]
        while nodes[-1] is not None:
            last = nodes[-1]
            node = self.factory.get_next(last.tags, lineage)
            nodes.append(node)
            if type(node) == StoryNode:
                for tag in node.tags:
                    if tag not in lineage:
                        lineage.append(tag)

        texts = [self.resolve_text(node.text)
                 for node in nodes if type(node) == StoryNode]
        text = ' '.join(texts)
        return text

    def resolve_text(self, text: str) -> str:
        _START = 'start'
        _END = 'END'
        _TXT = 'txt'
        pattern = r'#([a-zA-Z]+):([a-zA-Z]+):([a-zA-Z]+)\(([a-zA-Z]*)\)'

        matches = list(re.finditer(pattern, text))
        result = str(text)

        placeholders = []
        for match in matches:
            cat = match.group(1)
            typ = match.group(2)
            tag = match.group(3)
            var = match.group(4)
            start, end = match.span()

            try:
                node = self.resolver.resolve(cat, typ, tag)
                name = node.get_name(var)
                values = DefaultDict()
                values[_TXT] = name
                values[_START] = start
                values[_END] = end
                placeholders.append(values)
            except ValueError as ve:
                print('could not resolve placeholder')
                print(ve)

        for placeholder in reversed(placeholders):
            result = result[:placeholder[_START]] + placeholder[_TXT] + result[placeholder[_END]:]

        return result


if __name__ == '__main__':
    st = StoryTeller()
    text = st.tell_story()
    print()
    print(text)
    print()
    print('\tThe End')
    print()
