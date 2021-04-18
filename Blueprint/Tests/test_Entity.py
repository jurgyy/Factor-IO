from unittest import TestCase

import numpy as np

from Blueprint.Entity import EntityDict, Entity, CurvedRailEntity
from Blueprint.Position import PositionDict, Position


def get_entity_dict(entity_name: str, x: float, y: float, direction: int = 0) -> EntityDict:
    return EntityDict(entity_number=0, name=entity_name, position=PositionDict(x=x, y=y), direction=direction)


def get_entity(entity_name: str, x: float, y: float, direction: int = 0) -> Entity:
    return Entity(**get_entity_dict(entity_name, x, y, direction=direction))


class TestEntity(TestCase):
    def test_bounding_box_3x3(self):
        e = get_entity("assembling-machine-1", 0.5, 0.5)
        expected = np.array(([-1, 2], [-1, -1], [2, 2], [2, -1]))
        self.assertTrue(np.array_equal(e.bounding_box, expected), f"Expected:\n{expected}\nActual:\n{e.bounding_box}")

        e = get_entity("assembling-machine-1", 1.5, 1.5)
        expected = np.array(([0, 3], [0, 0], [3, 3], [3, 0]))
        self.assertTrue(np.array_equal(e.bounding_box, expected), f"Expected:\n{expected}\nActual:\n{e.bounding_box}")

        e = get_entity("assembling-machine-1", -0.5, -0.5)
        expected = np.array(([-2, 1], [-2, -2], [1, 1], [1, -2]))
        self.assertTrue(np.array_equal(e.bounding_box, expected), f"Expected:\n{expected}\nActual:\n{e.bounding_box}")

        e = get_entity("assembling-machine-1", -1.5, -1.5)
        expected = np.array(([-3, 0], [-3, -3], [0, 0], [0, -3]))
        self.assertTrue(np.array_equal(e.bounding_box, expected), f"Expected:\n{expected}\nActual:\n{e.bounding_box}")

    def test_bounding_box_2x2(self):
        e = get_entity("stone-furnace", 1, 1)
        expected = np.array(([0, 2], [0, 0], [2, 2], [2, 0]))
        self.assertTrue(np.array_equal(e.bounding_box, expected), f"Expected:\n{expected}\nActual:\n{e.bounding_box}")

    def test_bounding_box_1x2(self):
        e = get_entity("splitter", 1, 0.5)
        expected = np.array(([0, 1], [0, 0], [2, 1], [2, 0]))
        self.assertTrue(np.array_equal(e.bounding_box, expected), f"Expected:\n{expected}\nActual:\n{e.bounding_box}")

        e = get_entity("splitter", 2, 4.5)
        expected = np.array(([1, 5], [1, 4], [3, 5], [3, 4]))
        self.assertTrue(np.array_equal(e.bounding_box, expected), f"Expected:\n{expected}\nActual:\n{e.bounding_box}")

        e = get_entity("splitter", 0.5, 1, direction=2)
        expected = np.array(([0, 2], [0, 0], [1, 2], [1, 0]))
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


# noinspection DuplicatedCode
class TestCurvedRailEntity(TestCase):
    def test_bounding_box(self):
        e = CurvedRailEntity(**get_entity_dict("curved-rail", 3, 4))
        expected = np.array(([0, 8], [0, 0], [5, 8], [5, 0]))
        self.assertTrue(np.array_equal(expected, e.bounding_box), f"Expected:\n{expected}\nActual:\n{e.bounding_box}")

        e = CurvedRailEntity(**get_entity_dict("curved-rail", 3, 4, direction=5))
        expected = np.array(([0, 8], [0, 0], [5, 8], [5, 0]))
        self.assertTrue(np.array_equal(expected, e.bounding_box), f"Expected:\n{expected}\nActual:\n{e.bounding_box}")

        # Mirrored and 180 degrees rotated are one step off
        e = CurvedRailEntity(**get_entity_dict("curved-rail", 3, 4, direction=1))
        expected = np.array(([1, 8], [1, 0], [6, 8], [6, 0]))
        self.assertTrue(np.array_equal(expected, e.bounding_box), f"Expected:\n{expected}\nActual:\n{e.bounding_box}")

        e = CurvedRailEntity(**get_entity_dict("curved-rail", 3, 4, direction=4))
        expected = np.array(([1, 8], [1, 0], [6, 8], [6, 0]))
        self.assertTrue(np.array_equal(expected, e.bounding_box), f"Expected:\n{expected}\nActual:\n{e.bounding_box}")

        e = CurvedRailEntity(**get_entity_dict("curved-rail", 4, 3, direction=2))
        expected = np.array(([0, 5], [0, 0], [8, 5], [8, 0]))
        self.assertTrue(np.array_equal(expected, e.bounding_box), f"Expected:\n{expected}\nActual:\n{e.bounding_box}")

        e = CurvedRailEntity(**get_entity_dict("curved-rail", 4, 3, direction=7))
        expected = np.array(([0, 5], [0, 0], [8, 5], [8, 0]))
        self.assertTrue(np.array_equal(expected, e.bounding_box), f"Expected:\n{expected}\nActual:\n{e.bounding_box}")

        e = CurvedRailEntity(**get_entity_dict("curved-rail", 4, 3, direction=3))
        expected = np.array(([0, 6], [0, 1], [8, 6], [8, 1]))
        self.assertTrue(np.array_equal(expected, e.bounding_box), f"Expected:\n{expected}\nActual:\n{e.bounding_box}")

        e = CurvedRailEntity(**get_entity_dict("curved-rail", 4, 3, direction=6))
        expected = np.array(([0, 6], [0, 1], [8, 6], [8, 1]))
        self.assertTrue(np.array_equal(expected, e.bounding_box), f"Expected:\n{expected}\nActual:\n{e.bounding_box}")

    def test_bounding_box_through_origin(self):
        e = CurvedRailEntity(**get_entity_dict("curved-rail", 1, 2))
        expected = np.array(([-2, 6], [-2, -2], [3, 6], [3, -2]))
        self.assertTrue(np.array_equal(expected, e.bounding_box), f"Expected:\n{expected}\nActual:\n{e.bounding_box}")

        e = CurvedRailEntity(**get_entity_dict("curved-rail", 2, 1, direction=3))
        expected = np.array(([-2, 4], [-2, -1], [6, 4], [6, -1]))
        self.assertTrue(np.array_equal(expected, e.bounding_box), f"Expected:\n{expected}\nActual:\n{e.bounding_box}")

    def test_collision_masks(self):
        e = CurvedRailEntity(**get_entity_dict("curved-rail", 0, 0))
        expected = np.array([[False, True, False, False, False],
                             [True, True, True, False, False],
                             [False, True, True, True, False],
                             [False, True, True, True, False],
                             [False, False, True, True, True],
                             [False, False, False, True, True],
                             [False, False, False, True, True],
                             [False, False, False, True, True]], dtype=bool)
        self.assertTrue(np.array_equal(expected, e.get_collision_mask()),
                        f"Expected:\n{expected}\nActual:\n{e.get_collision_mask()}")

        e = CurvedRailEntity(**get_entity_dict("curved-rail", 0, 0, direction=1))
        expected = np.array([[False, False, False, True, False],
                             [False, False, True, True, True],
                             [False, True, True, True, False],
                             [False, True, True, True, False],
                             [True, True, True, False, False],
                             [True, True, False, False, False],
                             [True, True, False, False, False],
                             [True, True, False, False, False]], dtype=bool)
        self.assertTrue(np.array_equal(expected, e.get_collision_mask()),
                        f"Expected:\n{expected}\nActual:\n{e.get_collision_mask()}")

        e = CurvedRailEntity(**get_entity_dict("curved-rail", 0, 0, direction=2))
        expected = np.array([[False, False, False, False, False, False, True, False],
                             [False, False, False, False, True, True, True, True],
                             [False, False, False, True, True, True, True, False],
                             [True, True, True, True, True, True, False, False],
                             [True, True, True, True, False, False, False, False]], dtype=bool)
        self.assertTrue(np.array_equal(expected, e.get_collision_mask()),
                        f"Expected:\n{expected}\nActual:\n{e.get_collision_mask()}")

        e = CurvedRailEntity(**get_entity_dict("curved-rail", 0, 0, direction=3))
        expected = np.array([[True, True, True, True, False, False, False, False],
                             [True, True, True, True, True, True, False, False],
                             [False, False, False, True, True, True, True, False],
                             [False, False, False, False, True, True, True, True],
                             [False, False, False, False, False, False, True, False]], dtype=bool)
        self.assertTrue(np.array_equal(expected, e.get_collision_mask()),
                        f"Expected:\n{expected}\nActual:\n{e.get_collision_mask()}")

        e = CurvedRailEntity(**get_entity_dict("curved-rail", 0, 0, direction=4))
        expected = np.array([[True, True, False, False, False],
                             [True, True, False, False, False],
                             [True, True, False, False, False],
                             [True, True, True, False, False],
                             [False, True, True, True, False],
                             [False, True, True, True, False],
                             [False, False, True, True, True],
                             [False, False, False, True, False]], dtype=bool)
        self.assertTrue(np.array_equal(expected, e.get_collision_mask()),
                        f"Expected:\n{expected}\nActual:\n{e.get_collision_mask()}")

        e = CurvedRailEntity(**get_entity_dict("curved-rail", 0, 0, direction=5))
        expected = np.array([[False, False, False, True, True],
                             [False, False, False, True, True],
                             [False, False, False, True, True],
                             [False, False, True, True, True],
                             [False, True, True, True, False],
                             [False, True, True, True, False],
                             [True, True, True, False, False],
                             [False, True, False, False, False]], dtype=bool)
        self.assertTrue(np.array_equal(expected, e.get_collision_mask()),
                        f"Expected:\n{expected}\nActual:\n{e.get_collision_mask()}")

        e = CurvedRailEntity(**get_entity_dict("curved-rail", 0, 0, direction=6))
        expected = np.array([[False, False, False, False, True, True, True, True],
                             [False, False, True, True, True, True, True, True],
                             [False, True, True, True, True, False, False, False],
                             [True, True, True, True, False, False, False, False],
                             [False, True, False, False, False, False, False, False]], dtype=bool)
        self.assertTrue(np.array_equal(expected, e.get_collision_mask()),
                        f"Expected:\n{expected}\nActual:\n{e.get_collision_mask()}")

        e = CurvedRailEntity(**get_entity_dict("curved-rail", 0, 0, direction=7))
        expected = np.array([[False, True, False, False, False, False, False, False],
                             [True, True, True, True, False, False, False, False],
                             [False, True, True, True, True, False, False, False],
                             [False, False, True, True, True, True, True, True],
                             [False, False, False, False, True, True, True, True]], dtype=bool)
        self.assertTrue(np.array_equal(expected, e.get_collision_mask()),
                        f"Expected:\n{expected}\nActual:\n{e.get_collision_mask()}")
