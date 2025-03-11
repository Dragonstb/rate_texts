from rate_texts.dev_tools.story_teller.story_element_almanach import StoryElementAlmanach
from rate_texts.dev_tools.story_teller.story_element_node import StoryElementNode
from rate_texts.dev_tools.story_teller.entity_factory import EntityFactory
from rate_texts.dev_tools.story_teller.region_factory import RegionFactory
from typing import DefaultDict, List, Dict


class ResolvingStrategy:

    def resolve(self, tag: str, almanach: StoryElementAlmanach) -> StoryElementNode: ...


class NewElementResolver(ResolvingStrategy):
    """Creates a new entity and returns it"""

    def resolve(self, tag: str, almanach: StoryElementAlmanach) -> StoryElementNode:
        node = almanach.create_element(tag)
        return node


class OldElementResolver(ResolvingStrategy):
    """Returns an existing entity if possible. If not, a new entity is created."""

    def resolve(self, tag: str, almanach: StoryElementAlmanach) -> StoryElementNode:
        node = almanach.get_or_create_element(tag)
        return node


class StoryElementResolver:
    """
    Gets an entity based on the tags and the story usage type (new character, existing one, ...).
    """

    _OLD = 'old'
    _NEW = 'new'

    strategy: DefaultDict[str, ResolvingStrategy] = DefaultDict()
    almanach: StoryElementAlmanach

    def __init__(self, almanach: StoryElementAlmanach) -> None:
        self.almanach = almanach
        self.strategy[self._NEW] = NewElementResolver()
        self.strategy[self._OLD] = OldElementResolver()

    def resolve_element(self, typ: str, tag: str) -> StoryElementNode:
        """
        Gets an entity with the given tag and the given type of usage.

        typ: str
        Type of usage in the story. Is it a new entity? An entity that already has appeared befor? ...

        tag: str
        Tag the entity bears.

        return: StoryElementNode
        An entity node matching all requirements.

        raises: ValueError
        If 'typ' does not match a registered strategy of resolving the request for an entity.
        """
        if typ not in self.strategy.keys():
            raise ValueError(f'No strategy for resolving {typ}.')

        node = self.strategy[typ].resolve(tag, self.almanach)
        return node


class EntityResolverBuilder:

    _names: List[str]

    def __init__(self, names: List[str] | None) -> None:
        self._names = names if names is not None else []

    def add_names(self, names: List[str]) -> None:
        self._names = self._names + names

    def add_name(self, name: str) -> None:
        self._names.append(name)

    def build(self) -> StoryElementResolver:
        factory = EntityFactory(self._names)
        almanach = StoryElementAlmanach(factory)
        resolver = StoryElementResolver(almanach)
        return resolver


class RegionResolverBuilder:

    regions: List[DefaultDict | Dict]

    def __init__(self, regions: List[DefaultDict | Dict] = []) -> None:
        self.regions = regions

    def add_regions(self, regions: List[DefaultDict | Dict]) -> None:
        self.regions = self.regions + regions

    def add_region(self, region: DefaultDict | Dict) -> None:
        self.regions.append(region)

    def build(self) -> StoryElementResolver:
        factory = RegionFactory(self.regions)
        almanach = StoryElementAlmanach(factory)
        resolver = StoryElementResolver(almanach)
        return resolver
