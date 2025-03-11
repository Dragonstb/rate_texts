from typing import List


class StoryNode:

    tags: List[str]
    """Tags related to this story node."""
    text: str
    """The text of the story node"""
    follows_on_tags: List[str]
    """
    List of all tags the preceeding node must have for this node to become the successor. The preceding node may have
    more tags assigned, but must not miss out any of the tags listed in this field.
    """
    in_lineage_of: List[str]
    """
    This node can  only be picked when all these tags appear on any of the previous nodes in the story.
    The tags do not have to be on the the same node, though.
    """

    def __init__(self, tags: List[str], text: str, follows_on: List[str] = [], in_lineage_of: List[str] = []) -> None:
        self.tags = tags
        self.text = text
        self.follows_on_tags = follows_on
        self.in_lineage_of = in_lineage_of

