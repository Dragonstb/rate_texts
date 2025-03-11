from typing import List, DefaultDict, Dict
from rate_texts.dev_tools.story_teller.story_node import StoryNode
from rate_texts.dev_tools import utils
import numpy as np
import copy


class StoryFactory:

    story_fragments: DefaultDict
    initial_fragments: List[StoryNode]
    _TEXT = 'text'
    _TAGS = 'tags'
    _FOLLOWS_ON = 'follows_on'
    _LINEAGE_OF = 'lineage_of'

    def __init__(self, json: List[DefaultDict | Dict]) -> None:

        self.initial_fragments = []
        self.story_fragments = DefaultDict()

        nodes = [self._convert_to_node(entry) for entry in json]
        for node in nodes:
            if len(node.follows_on_tags) > 0:
                for follows in node.follows_on_tags:
                    if follows not in self.story_fragments.keys():
                        self.story_fragments[follows] = []
                    self.story_fragments[follows].append(node)
            else:
                # story fragments without requirements on the tags of the preceding node
                # can only be picked at the very beginning of the story
                self.initial_fragments.append(node)

    def _convert_to_node(self, dict: DefaultDict | Dict) -> StoryNode:
        text = dict[self._TEXT]
        tags = dict[self._TAGS]
        follows = dict[self._FOLLOWS_ON] if self._FOLLOWS_ON in dict.keys() else []
        lineage = dict[self._LINEAGE_OF] if self._LINEAGE_OF in dict.keys() else []
        node = StoryNode(tags, text, follows, lineage)
        return node

    def get_next(self, predecesor_tags: List[str], lineage: list[str]) -> StoryNode | None:
        """
        Gets the next node.

        tags: List[str]
        Tags of the last node. Only story fragments with all predecessor tags in 'tags' can
        be picked here.

        lineage: List[str]
        List of all tags that have appeared on the nodes in the story so far.

        returns: StoryNode | None
        Deep copy of the story node picked, or None if no story node could be found.
        """
        # TODO: better coding
        candidates = []
        for tag in predecesor_tags:
            if tag not in self.story_fragments.keys() or len(self.story_fragments[tag]) == 0:
                continue

            for node in self.story_fragments[tag]:
                if node in candidates:
                    continue

                ok = True
                for demanded in node.follows_on_tags:
                    if demanded not in predecesor_tags:
                        ok = False
                        break
                if ok:
                    for demanded in node.in_lineage_of:
                        if demanded not in lineage:
                            ok = False
                            break
                if ok:
                    candidates.append(node)

        if len(candidates) > 0:
            idx = utils.pick_from_array(np.arange(len(candidates)))
            node = candidates[idx]
            return copy.deepcopy(node)
        else:
            return None

    def get_initial(self) -> StoryNode | None:
        if len(self.initial_fragments) > 0:
            idx = utils.pick_from_array(np.arange(len(self.initial_fragments)))
            node = self.initial_fragments[idx]
            return copy.deepcopy(node)
        else:
            return None
