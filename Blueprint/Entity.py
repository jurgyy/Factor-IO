import json
from typing import List
from math import cos, sin
import numpy as np

from typing_extensions import TypedDict

import utils
from Blueprint.Color import Color, ColorDict
from Blueprint.Connection import Connection, ConnectionDict
from Blueprint.InfinitySettings import InfinitySettings, InfinitySettingsDict
from Blueprint.Inventory import Inventory, InventoryDict
from Blueprint.ItemFilter import ItemFilter, ItemFilterDict
from Blueprint.LogisticFilter import LogisticFilter, LogisticFilterDict
from Blueprint.Position import Position, PositionDict
from Blueprint.SpeakerAlertParameter import SpeakerAlertParameter, SpeakerAlertParameterDict
from Blueprint.SpeakerParameter import SpeakerParameter, SpeakerParameterDict
from cachedProperty import cached_property
from config import Config


class EntityDict(TypedDict):
    entity_number: int
    name: str
    position: PositionDict
    direction: int
    orientation: float
    connections: ConnectionDict
    control_behavior: object
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
    _entity_size_dict: dict = None

    @staticmethod
    def get_entity_size_dict() -> dict:
        if Entity._entity_size_dict is None:
            with open(Config.EntitySizeJsonFName) as f:
                Entity._entity_size_dict = json.load(f)

        return Entity._entity_size_dict

    def __init__(self,
                 entity_number: int,
                 name: str,
                 position: PositionDict,
                 direction: int = None,
                 orientation: float = None,
                 connections: ConnectionDict = None,
                 control_behavior: object = None,
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
        self.direction: int = 0 if direction is None else direction
        self.orientation: float = orientation
        self.connections: Connection = None if connections is None else Connection(**connections)
        self.control_behavior: object = control_behavior
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

        (x, y), (w, h) = Entity.get_entity_size_dict()[self.name]
        self.half_width = w
        self.half_height = h

    def __repr__(self):
        return f"[Entity {self.name}@{self.position} D={self.direction}]"

    @cached_property
    def bounding_box(self) -> np.ndarray:
        if self.direction % 2 == 0:
            # 90 degree turns
            x_dist, y_dist = self.half_width, self.half_height

            if self.direction % 4 != 0:
                x_dist, y_dist = y_dist, x_dist

            min_x = round(self.position.x - x_dist)
            max_x = round(self.position.x + x_dist)
            min_y = round(self.position.y - y_dist)
            max_y = round(self.position.y + y_dist)

            corners = np.array([[min_x, min_x, max_x, max_x], [min_y, max_y, min_y, max_y]])

            return corners.T

        else:
            # 45 degree turns
            raise NotImplementedError("45 degree turns not supported yet")
            # degrees = self.direction * 45
            # theta = np.deg2rad(360 - degrees)
            # return utils.math.rotate(np.array([self.position.x, self.position.y]), corners, theta).T






