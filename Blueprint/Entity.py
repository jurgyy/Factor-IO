import json
from typing import List, Tuple, Type
import numpy as np

from typing_extensions import TypedDict

from Blueprint.Color import Color, ColorDict
from Blueprint.Connection import Connection, ConnectionDict
from Blueprint.Exceptions.UnknownEntityException import UnknownEntityException
from Blueprint.InfinitySettings import InfinitySettings, InfinitySettingsDict
from Blueprint.Inventory import Inventory, InventoryDict
from Blueprint.ItemFilter import ItemFilter, ItemFilterDict
from Blueprint.LogisticFilter import LogisticFilter, LogisticFilterDict
from Blueprint.Position import Position, PositionDict
from Blueprint.SpeakerAlertParameter import SpeakerAlertParameter, SpeakerAlertParameterDict
from Blueprint.SpeakerParameter import SpeakerParameter, SpeakerParameterDict
from Blueprint.FactorioBlueprintObject import FactorioBlueprintObject
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
    neighbours: List[int]
    buffer_size: int
    power_production: int
    power_usage: int
    switch_state: bool
    manual_trains_limit: int
    signal: object  # Found in -LY2k2uaRpsSKNDlffKk, not sure what type it is.


class Entity(FactorioBlueprintObject):
    dict_type: Type[TypedDict] = EntityDict
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
                 neighbours: List[int] = (),
                 buffer_size: int = None,
                 power_production: int = None,
                 power_usage: int = None,
                 switch_state: bool = None,
                 manual_trains_limit: int = None,
                 signal: object = None
                 ):
        if name not in self.get_entity_size_dict():
            raise UnknownEntityException(name)

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
        self.neighbours: List[int] = list(neighbours)
        self.buffer_size: int = buffer_size
        self.power_production: int = power_production
        self. power_usage: int = power_usage
        self.switch_state: bool = switch_state
        self.manual_trains_limit: int = manual_trains_limit
        self.signal: object = signal

        if self.direction > 7:
            raise Exception("Invalid direction")

        self._init_dimensions()
        self._correct_position()

    def __repr__(self):
        return f"[Entity {self.name}@{self.position} D={self.direction}]"

    def _init_dimensions(self):
        self._orientate_half_dimensions(Entity.get_entity_size_dict()[self.name])

    def _orientate_half_dimensions(self, dimension_tuple: Tuple[Tuple[float, float], Tuple[float, float]]):
        (l, d), (r, u) = dimension_tuple
        if self.direction == 0 or self.direction == 5:
            # 0: Upright
            # 5: Mirror then rotate 180 clockwise
            w, h = (l, r), (d, u)
        elif self.direction == 1 or self.direction == 4:
            # 1: Mirror horizontally
            # 4: Rotate 180 clockwise
            w, h = (-r, -l), (d, u)
        elif self.direction == 2 or self.direction == 7:
            # 2: Rotate 90 degree clockwise
            # 7: Mirror then rotate 270 clockwise
            w, h = (d, u), (l, r)
        else:
            # 3: Mirror then rotate 90 clockwise
            # 6: Rotate 270 clockwise
            w, h = (-u, -d), (-r, -l)

        self.half_width: Tuple[float, float] = w
        self.half_height: Tuple[float, float] = h

    @cached_property
    def bounding_box(self) -> np.ndarray:
        """
        Returns 4 tuples in the order of bottom left, top left, bottom right, top right.
        In Factorio the y-axis increases when going down so the bottom row has the max_y value.
        """
        (l, r), (d, u) = self.half_width, self.half_height

        min_x = int(Entity._round_corrected(self.position.x + l))
        max_x = int(Entity._round_corrected(self.position.x + r))
        min_y = int(Entity._round_corrected(self.position.y + d))
        max_y = int(Entity._round_corrected(self.position.y + u))

        return self._get_corners(max_x, max_y, min_x, min_y)

    @staticmethod
    def _get_corners(max_x, max_y, min_x, min_y):
        return np.array([[min_x, max_y],
                         [min_x, min_y],
                         [max_x, max_y],
                         [max_x, min_y]])

    @staticmethod
    def _round_to_corrected_halve(value: float):
        # About 3 times faster than using np.floor
        if value <= -0.00390625:
            # value - 1/256
            # see https://forums.factorio.com/viewtopic.php?f=23&t=97568&p=542718
            return int(value + 0.00390625) - 0.5
        if value < 0:
            value -= 1
        return int(value) + 0.5

    @staticmethod
    def _round_corrected(value: float):
        # About 4 times faster than using np.floor
        if value < -0.5:
            return int(value + 0.5) - 1
        return int(value + 0.5)

    def _correct_position(self):
        """"
            1x1 = (0.5, 0.5)
            1x2 = (1,   0.5)
            2x2 = (1,     1)
            3x3 = (1.5, 1.5)
            4x4 = (2,     2)
            9x9 = (4.5, 4.5)
        """
        width = round(self.half_width[1] - self.half_width[0])
        height = round(self.half_height[1] - self.half_height[0])

        if width % 2 == 0:
            self.position.x = self._round_corrected(self.position.x)
        else:
            self.position.x = self._round_to_corrected_halve(self.position.x)

        if height % 2 == 0:
            self.position.y = self._round_corrected(self.position.y)
        else:
            self.position.y = self._round_to_corrected_halve(self.position.y)

    def get_collision_mask(self):
        width = int(round((self.half_width[1] - self.half_width[0]) * 2) / 2)
        height = int(round((self.half_height[1] - self.half_height[0]) * 2) / 2)

        if self.direction == 2 or self.direction == 6:
            # direction = rotated 90 or 270 degrees
            width, height = height, width

        return np.ones((height, width), dtype=bool)


class CurvedRailEntity(Entity):
    dict_type: Type[TypedDict] = EntityDict

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
                 station: str = None
                 ):
        if name != "curved-rail":
            raise Exception("CurvedRailEntity can only be created for curved-rail")
        super().__init__(entity_number, name, position, direction, orientation, connections, control_behavior, items,
                         recipe, bar, inventory, infinity_settings, type, input_priority, output_priority, filter,
                         filters, filter_mode, override_stack_size, drop_position, pickup_position, request_filters,
                         request_from_buffers, parameters, alert_parameters, auto_launch, variation, color, station)

    def _init_dimensions(self):
        (l, r), (d, u) = (-3, 2), (-4, 4)
        self._orientate_half_dimensions(((l, d), (r, u)))

    def get_collision_mask(self):
        mask = np.array([[False, True, False, False, False],
                         [True, True, True, False, False],
                         [False, True, True, True, False],
                         [False, True, True, True, False],
                         [False, False, True, True, True],
                         [False, False, False, True, True],
                         [False, False, False, True, True],
                         [False, False, False, True, True]], dtype=bool)
        if self.direction == 0:
            return mask
        elif self.direction == 1:
            # Mirror horizontally
            return np.flip(mask, axis=1)
        elif self.direction == 2:
            # Rotate 90 degree clockwise
            return np.rot90(mask, k=3)
        elif self.direction == 3:
            # Mirror then rotate 90 clockwise
            return np.rot90(np.flip(mask, axis=1), k=3)
        elif self.direction == 4:
            # Rotate 180 clockwise
            return np.rot90(mask, k=2)
        elif self.direction == 5:
            # Mirror then rotate 180 clockwise
            return np.flip(mask, axis=0)
        elif self.direction == 6:
            # Rotate 270 clockwise
            return np.rot90(mask)
        elif self.direction == 7:
            # Mirror then rotate 270 clockwise
            return np.rot90(np.flip(mask, axis=1))

    def _correct_position(self):
        # Curved Rails are always centered at rounded values.
        self.position.x = self._round_corrected(self.position.x)
        self.position.y = self._round_corrected(self.position.y)
