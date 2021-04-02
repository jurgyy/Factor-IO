from unittest import TestCase

import numpy as np

from Blueprint.Entity import EntityDict, Entity
from Blueprint.Position import PositionDict


def get_entity_dict(entity_name: str, x: float, y: float, direction: int = 0) -> EntityDict:
    return EntityDict(entity_number=0, name=entity_name, position=PositionDict(x=x, y=y), direction=direction)


def get_entity(entity_name: str, x: float, y: float, direction: int = 0) -> Entity:
    return Entity(**get_entity_dict(entity_name, x, y, direction=direction))


class TestEntity(TestCase):
    def test_bounding_box_3x3(self):
        e = get_entity("assembling-machine-1", 0.5, 0.5)
        expected = np.array(([-1, -1], [-1, 2], [2, -1], [2, 2]))
        self.assertTrue(np.array_equal(e.bounding_box, expected), f"Expected: {expected}\nActual: {e.bounding_box}")

        e = get_entity("assembling-machine-1", 1.5, 1.5)
        expected = np.array(([0, 0], [0, 3], [3, 0], [3, 3]))
        self.assertTrue(np.array_equal(e.bounding_box, expected), f"Expected: {expected}\nActual: {e.bounding_box}")

        e = get_entity("assembling-machine-1", -0.5, -0.5)
        expected = np.array(([-2, -2], [-2, 1], [1, -2], [1, 1]))
        self.assertTrue(np.array_equal(e.bounding_box, expected), f"Expected: {expected}\nActual: {e.bounding_box}")

        e = get_entity("assembling-machine-1", -1.5, -1.5)
        expected = np.array(([-3, -3], [-3, 0], [0, -3], [0, 0]))
        self.assertTrue(np.array_equal(e.bounding_box, expected), f"Expected: {expected}\nActual: {e.bounding_box}")

    def test_bounding_box_1x2(self):
        e = get_entity("splitter", 1, 0.5)
        expected = np.array(([0, 0], [0, 1], [2, 0], [2, 1]))
        self.assertTrue(np.array_equal(e.bounding_box, expected), f"Expected: {expected}\nActual: {e.bounding_box}")

        e = get_entity("splitter", 0.5, 1, direction=2)
        expected = np.array(([0, 0], [0, 2], [1, 0], [1, 2]))
        self.assertTrue(np.array_equal(e.bounding_box, expected), f"Expected: {expected}\nActual: {e.bounding_box}")



