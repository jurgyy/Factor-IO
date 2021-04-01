from typing import List

from typing_extensions import TypedDict

from Blueprint.Color import Color, ColorDict
from Blueprint.Connection import Connection, ConnectionDict
from Blueprint.InfinitySettings import InfinitySettings, InfinitySettingsDict
from Blueprint.Inventory import Inventory, InventoryDict
from Blueprint.ItemFilter import ItemFilter, ItemFilterDict
from Blueprint.LogisticFilter import LogisticFilter, LogisticFilterDict
from Blueprint.Position import Position, PositionDict
from Blueprint.SpeakerAlertParameter import SpeakerAlertParameter, SpeakerAlertParameterDict
from Blueprint.SpeakerParameter import SpeakerParameter, SpeakerParameterDict


class EntityDict(TypedDict):
    entity_number: int
    name: str
    position: PositionDict
    direction: int
    orientation: float
    connections: ConnectionDict
    control_behaviour: object
    items: object
    recipe: str
    bar: int
    inventory: InventoryDict
    infinity_settings: InfinitySettingsDict
    type: str
    input_priority: str
    output_priority: str
    filter: str
    filters: List[ItemFilterDict]
    filter_mode: str
    override_stack_size: int
    drop_position: PositionDict
    pickup_position: PositionDict
    request_filters: List[LogisticFilterDict]
    request_from_buffers: bool
    parameters: SpeakerParameterDict
    alert_parameters: SpeakerAlertParameterDict
    auto_launch: bool
    variation: object
    color: ColorDict
    station: str


class Entity:
    def __init__(self,
                 entity_number: int,
                 name: str,
                 position: PositionDict,
                 direction: int = None,
                 orientation: float = None,
                 connections: ConnectionDict = None,
                 control_behaviour: object = None,
                 items: object = None,
                 recipe: str = None,
                 bar: int = None,
                 inventory: InventoryDict = None,
                 infinity_settings: InfinitySettingsDict = None,
                 type: str = None,
                 input_priority: str = None,
                 output_priority: str = None,
                 filter: str = None,
                 filters: List[ItemFilterDict] = (),
                 filter_mode: str = None,
                 override_stack_size: int = None,
                 drop_position: PositionDict = None,
                 pickup_position: PositionDict = None,
                 request_filters: List[LogisticFilterDict] = (),
                 request_from_buffers: bool = None,
                 parameters: SpeakerParameterDict = None,
                 alert_parameters: SpeakerAlertParameterDict = None,
                 auto_launch: bool = None,
                 variation: object = None,
                 color: ColorDict = None,
                 station: str = None,
                 ):
        self.entity_number: int = entity_number
        self.name: str = name
        self.position: Position = Position(**position)
        self.direction: int = direction
        self.orientation: float = orientation
        self.connections: Connection = None if connections is None else Connection(**connections)
        self.control_behaviour: object = control_behaviour
        self.items: object = items
        self.recipe: str = recipe
        self.bar: int = bar
        self.inventory: Inventory = None if inventory is None else Inventory(**inventory)
        self.infinity_settings: InfinitySettings = None if infinity_settings is None else InfinitySettings(**infinity_settings)
        self.type: str = type
        self.input_priority: str = input_priority
        self.output_priority: str = output_priority
        self.filter: str = filter
        self.filters: List[ItemFilter] = [ItemFilter(**f) for f in filters]
        self.filter_mode: str = filter_mode
        self.override_stack_size: int = override_stack_size
        self.drop_position: Position = None if drop_position is None else Position(**drop_position)
        self.pickup_position: Position = None if pickup_position is None else Position(**pickup_position)
        self.request_filters: List[LogisticFilter] = [LogisticFilter(**f) for f in request_filters]
        self.request_from_buffers: bool = request_from_buffers
        self.parameters: SpeakerParameter = None if parameters is None else SpeakerParameter(**parameters)
        self.alert_parameters: SpeakerAlertParameter = None if alert_parameters is None else SpeakerAlertParameter(**alert_parameters)
        self.auto_launch: bool = auto_launch
        self.variation: object = variation
        self.color: Color = None if color is None else Color(**color)
        self.station: str = station

    def __repr__(self):
        return f"[Entity {self.name}@{self.position}]"
