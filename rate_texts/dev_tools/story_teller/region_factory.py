from typing import List, DefaultDict, Dict
import rate_texts.dev_tools.utils as utils
from rate_texts.dev_tools.story_teller.region_node import RegionNode
from rate_texts.dev_tools.story_teller.story_element_factory import StoryElementFactory
import numpy as np


class RegionFactory(StoryElementFactory):

    _NAME = 'name'
    _PLACES = 'places'
    regions: List[DefaultDict | Dict] = []

    def __init__(self, regions: List[DefaultDict | Dict] = []) -> None:
        self.regions = regions

    def make_new(self, tags: List[str] = []) -> RegionNode:
        """
        Creates a new region node with a randomly chosen region.

        tags: List[str] = []
        Tags for the region.

        returns: RegionNode
        A new RegionNode
        """
        region = self._pick()
        node = RegionNode(region[self._NAME], region[self._PLACES], tags)
        return node

    def _pick(self) -> DefaultDict:
        idx = utils.pick_from_array(np.arange(len(self.regions)))
        return self.regions[idx]
