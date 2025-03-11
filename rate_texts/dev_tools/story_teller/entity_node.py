from typing import DefaultDict, List
from rate_texts.dev_tools.story_teller.story_element_node import StoryElementNode

_DEFAULT = 'default'
_GEN = 'g'


class EntityNode(StoryElementNode):

    name_variants: DefaultDict
    """The character's name. Each entry relates to a grammatical variation of the name, like case or cardinallity."""

    tags: List[str]
    """Tags associated with this character."""

    def __init__(self, name: str, tags: List[str] = []) -> None:
        self.name = DefaultDict()
        self.name[_DEFAULT] = name
        self.name[_GEN] = "'".join(
            [name, "s"]) if name[-1] not in ['s', 'x'] and name[-2:] != 'th' else name+"'"

        self.tags = tags

    def get_name(self, variant: str | None = _DEFAULT) -> str:
        """
        Returns the name in the requested grammatical variant.

        variant: str = 'default'
        The key to the grammatical variant. If there is no variant for this key, the default
        name is retuned.

        returns: str
        The name in the requested grammatical variant.
        """
        return self.name[variant] if variant is not None and variant in self.name.keys() else self.name[_DEFAULT]
