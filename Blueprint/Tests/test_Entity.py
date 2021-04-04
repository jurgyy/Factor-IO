from unittest import TestCase

import numpy as np

from Blueprint.Entity import EntityDict, Entity
from Blueprint.Position import PositionDict, Position


def get_entity_dict(entity_name: str, x: float, y: float, direction: int = 0) -> EntityDict:
    return EntityDict(entity_number=0, name=entity_name, position=PositionDict(x=x, y=y), direction=direction)


def get_entity(entity_name: str, x: float, y: float, direction: int = 0) -> Entity:
    return Entity(**get_entity_dict(entity_name, x, y, direction=direction))


class TestEntity(TestCase):
    def test_bounding_box_3x3(self):
        e = get_entity("assembling-machine-1", 0.5, 0.5)
        expected = np.array(([-1, -1], [-1, 2], [2, -1], [2, 2]))
        self.assertTrue(np.array_equal(e.bounding_box, expected), f"Expected:\n{expected}\nActual:\n{e.bounding_box}")

        e = get_entity("assembling-machine-1", 1.5, 1.5)
        expected = np.array(([0, 0], [0, 3], [3, 0], [3, 3]))
        self.assertTrue(np.array_equal(e.bounding_box, expected), f"Expected:\n{expected}\nActual:\n{e.bounding_box}")

        e = get_entity("assembling-machine-1", -0.5, -0.5)
        expected = np.array(([-2, -2], [-2, 1], [1, -2], [1, 1]))
        self.assertTrue(np.array_equal(e.bounding_box, expected), f"Expected:\n{expected}\nActual:\n{e.bounding_box}")

        e = get_entity("assembling-machine-1", -1.5, -1.5)
        expected = np.array(([-3, -3], [-3, 0], [0, -3], [0, 0]))
        self.assertTrue(np.array_equal(e.bounding_box, expected), f"Expected:\n{expected}\nActual:\n{e.bounding_box}")

    def test_bounding_box_1x2(self):
        e = get_entity("splitter", 1, 0.5)
        expected = np.array(([0, 0], [0, 1], [2, 0], [2, 1]))
        self.assertTrue(np.array_equal(e.bounding_box, expected), f"Expected:\n{expected}\nActual:\n{e.bounding_box}")

        e = get_entity("splitter", 2, 4.5)
        expected = np.array(([1, 4], [1, 5], [3, 4], [3, 5]))
        self.assertTrue(np.array_equal(e.bounding_box, expected), f"Expected:\n{expected}\nActual:\n{e.bounding_box}")

        e = get_entity("splitter", 0.5, 1, direction=2)
        expected = np.array(([0, 0], [0, 2], [1, 0], [1, 2]))
        self.assertTrue(np.array_equal(e.bounding_box, expected), f"Expected:\n{expected}\nActual:\n{e.bounding_box}")

    def test_correct_position(self):
        self.assertEqual(Position(1.5, 1.5), get_entity("assembling-machine-1", 1.5, 1.5).position)

        self.assertEqual(Position(1, 0.5), get_entity("splitter", 1, 0.5).position)
        self.assertEqual(Position(0, 0.5), get_entity("splitter", -0.5, 0).position)

        self.assertEqual(Position(0.5, 0.5), get_entity("transport-belt", 0.5, 0.5).position)

    def test_round_corrected(self):
        self.assertEqual(0, Entity._round_corrected(-0.5))
        self.assertEqual(1, Entity._round_corrected(0.5))

    def test_round_to_corrected_halve(self):
        self.assertEqual(0.5, Entity._round_to_corrected_halve(0))
        self.assertEqual(0.5, Entity._round_to_corrected_halve(0.2))
        self.assertEqual(0.5, Entity._round_to_corrected_halve(0.4))
        self.assertEqual(0.5, Entity._round_to_corrected_halve(0.6))
        self.assertEqual(0.5, Entity._round_to_corrected_halve(0.8))
        self.assertEqual(0.5, Entity._round_to_corrected_halve(0.99))
        self.assertEqual(1.5, Entity._round_to_corrected_halve(1))
        self.assertEqual(1.5, Entity._round_to_corrected_halve(1.1))
        self.assertEqual(1.5, Entity._round_to_corrected_halve(1.5))
        self.assertEqual(1.5, Entity._round_to_corrected_halve(1.99))
        self.assertEqual(2.5, Entity._round_to_corrected_halve(2))

        self.assertEqual(-0.5, Entity._round_to_corrected_halve(-0.2))
        self.assertEqual(-0.5, Entity._round_to_corrected_halve(-0.4))
        self.assertEqual(-0.5, Entity._round_to_corrected_halve(-0.6))
        self.assertEqual(-0.5, Entity._round_to_corrected_halve(-0.8))
        self.assertEqual(-0.5, Entity._round_to_corrected_halve(-0.99))
        self.assertEqual(-0.5, Entity._round_to_corrected_halve(-1))
        self.assertEqual(-1.5, Entity._round_to_corrected_halve(-1.5))
        self.assertEqual(-1.5, Entity._round_to_corrected_halve(-1.99))
        self.assertEqual(-1.5, Entity._round_to_corrected_halve(-2))
        self.assertEqual(-2.5, Entity._round_to_corrected_halve(-2.1))



