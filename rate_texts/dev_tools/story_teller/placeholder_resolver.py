from typing import DefaultDict
from rate_texts.dev_tools.story_teller.story_element_resolver import StoryElementResolver
from rate_texts.dev_tools.story_teller.story_element_node import StoryElementNode


class PlaceholderResolver:
    """
    Resolves placeholders in the story to story element nodes. Depending on the category
    of the placeholder (character, twown, ...), another strategy is used to resolve the
    story element based on the properties of the placeholder.
    """

    strategies: DefaultDict[str, StoryElementResolver] = DefaultDict()

    def set_strategy_for(self, cat: str, resolver: StoryElementResolver) -> None:
        self.strategies[cat] = resolver

    def resolve(self, cat: str, typ: str, tag: str) -> StoryElementNode:
        """
        Resolves the placeholder into a story element node. This node may exist already or may
        be created, depending on the properties of the palceholder and the progress of the story.

        cat: str
        Category of the placeholder. Thsi describes if we look for a character, a town, ...

        typ: str
        The story usage type. Do we look for an existing character? Or rather a new one? ...

        tag: str
        Tags the node must bear to be picked. If a new one is created, it is attributed with these tags.

        returns: StroyElementNode
        A node with the demanded properties. It is garantueed thata  node is returned as long no error occurs.
        If absolutely necessary, a new node is created and returned. This can happen, for example, if an existing
        node is requested, but there is no node with the demanded properties.

        raises: ValueError
        If no strategies for resolving the category or the story usage type are registered.
        """
        if cat not in self.strategies.keys():
            raise ValueError(
                f'No strategy for story element category {cat} registered.')

        node = self.strategies[cat].resolve_element(typ, tag)
        return node
