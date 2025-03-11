import numpy as np
from typing import List
from rate_texts.dev_tools.story_teller.entity_node import EntityNode
from rate_texts.dev_tools.story_teller.story_element_factory import StoryElementFactory
import rate_texts.dev_tools.utils as utils
import copy


class EntityFactory(StoryElementFactory):

    availible_names: List[str]
    """Available names for entities. Picking a name depletes this list"""
    depleted_names: List[str]

    def __init__(self, names: List[str] = []) -> None:
        self.availible_names = copy.copy(names)
        self.depleted_names = []

    def make_new(self, tags: List[str] = []) -> EntityNode:
        """
        Creates a new entity node with a randomly picked name and the tags provided in the argument.

        tags: List[str] = []
        Tags for the entity node.

        returns: EntityNode
        The new Entity node

        raises: RuntimeError
        When the pool has no names left
        """
        name = self._extract_from_pool()
        node = EntityNode(name, tags)
        return node

    def _extract_from_pool(self) -> str:
        if len(self.availible_names) < 1:
            self.availible_names = self.depleted_names
            self.depleted_names = []

        idx = utils.pick_from_array(np.arange(len(self.availible_names)))
        name = self.availible_names.pop(idx)
        self.depleted_names.append(name)
        return name

        