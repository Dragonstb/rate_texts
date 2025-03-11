from typing import List, DefaultDict
from rate_texts.dev_tools.story_teller.story_element_factory import StoryElementFactory
from rate_texts.dev_tools.story_teller.story_element_node import StoryElementNode


class StoryElementAlmanach:
    """Keeps track of story element nodes used in the story."""

    factory: StoryElementFactory
    elements: DefaultDict[str, List[StoryElementNode]]
    count: int

    def __init__(self, factory: StoryElementFactory) -> None:
        self.factory = factory
        self.elements = DefaultDict()
        self.count = 0

    def get_or_create_element(self, tag: str) -> StoryElementNode:
        """
        Returns an entity bearing the demanded tag. If such an entity exist already, it is returned.
        If no such entity exists so far, a new one is created.

        tag: str
        Tag for the new node

        returns: StoryElementNode
        The new node.
        """
        # TODO: get entities that have multiple tags
        # TODO: possibility of getting all entities with the tags
        if tag in self.elements.keys():
            return self.elements[tag][-1]

        node = self.create_element(tag)
        return node

    def create_element(self, tag: str) -> StoryElementNode:
        """
        Invents and registers a new entity with the given tag.

        tag: str
        Tag for the new node

        returns: StoryElementNode
        The new node.
        """
        node = self.factory.make_new([tag])
        if tag in self.elements.keys():
            self.elements[tag].append(node)
        else:
            self.elements[tag] = [node]
        self.count = self.count + 1
        return node

    def count_elements(self) -> int:
        return self.count
