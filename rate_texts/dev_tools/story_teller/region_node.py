from typing import List, DefaultDict, Dict
import rate_texts.dev_tools.utils as utils
import numpy as np
import numpy.typing as npt
from rate_texts.dev_tools.story_teller.story_element_node import StoryElementNode


class RegionNode(StoryElementNode):

    name: str
    """name of the region"""
    variants: DefaultDict[str, npt.NDArray[np.str_]]
    """Some ways to describe how a point is located relative to the region"""
    tags: List[str]
    """Tags associated with that region"""

    def __init__(self, name: str, places: List[str] = [], tags: List[str] = []) -> None:
        self.name = name
        self.tags = tags
        self.variants = DefaultDict()
        if len(places) > 0:
            self.variants['places'] = np.array(places)

    def get_name(self, variant: str | None = None) -> str:
        if variant is None:
            return self.name
        elif variant in self.variants.keys():
            return utils.pick_from_array(self.variants[variant])
        else:
            return self.name
