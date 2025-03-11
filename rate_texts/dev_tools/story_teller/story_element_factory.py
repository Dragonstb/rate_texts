from rate_texts.dev_tools.story_teller.story_element_node import StoryElementNode
from typing import List


class StoryElementFactory:

    def make_new(self, tags: List[str] = []) -> StoryElementNode: ...
