from unittest import TestCase

from Blueprint.Blueprint import BlueprintDict, Blueprint
from Blueprint.Tests.test_Entity import get_entity_dict
from Grid import Grid


class TestGrid(TestCase):
    def test_single_1x1(self):
        bp = Blueprint(**BlueprintDict(entities=[
            get_entity_dict("transport-belt", 0.5, 0.5),
        ]))
        g = Grid(bp)
        self.assertEqual(1, g.width)
        self.assertEqual(1, g.height)
        self.assertEqual(bp.entities[0], g[0, 0])

        bp = Blueprint(**BlueprintDict(entities=[
            get_entity_dict("transport-belt", 1.5, 0.5),
        ]))
        g = Grid(bp)
        self.assertEqual(1, g.width)
        self.assertEqual(1, g.height)
        self.assertEqual(bp.entities[0], g[0, 0])

        bp = Blueprint(**BlueprintDict(entities=[
            get_entity_dict("transport-belt", -0.5, 0.5),
        ]))
        g = Grid(bp)
        self.assertEqual(1, g.width)
        self.assertEqual(1, g.height)
        self.assertEqual(bp.entities[0], g[0, 0])

        bp = Blueprint(**BlueprintDict(entities=[
            get_entity_dict("transport-belt", -1.5, 0.5),
        ]))
        g = Grid(bp)
        self.assertEqual(1, g.width)
        self.assertEqual(1, g.height)
        self.assertEqual(bp.entities[0], g[0, 0])

    def test_multiple_1x1(self):
        bp = Blueprint(**BlueprintDict(entities=[
            get_entity_dict("transport-belt", 0.5, 0.5),
            get_entity_dict("transport-belt", 1.5, 1.5),
        ]))
        g = Grid(bp)
        self.assertEqual(2, g.width)
        self.assertEqual(2, g.height)
        self.assertEqual(bp.entities[0], g[0, 0])
        self.assertEqual(bp.entities[1], g[1, 1])
        self.assertIsNone(g[0, 1])
        self.assertIsNone(g[1, 0])

        bp = Blueprint(**BlueprintDict(entities=[
            get_entity_dict("transport-belt", -2.5, -2.5),
            get_entity_dict("transport-belt", -2.5, 2.5),
            get_entity_dict("transport-belt", 2.5, -2.5),
            get_entity_dict("transport-belt", 2.5, 2.5),
        ]))
        g = Grid(bp)
        self.assertEqual(6, g.width)
        self.assertEqual(6, g.height)
        self.assertEqual(bp.entities[0], g[0, 0])
        self.assertEqual(bp.entities[1], g[0, 5])
        self.assertEqual(bp.entities[2], g[5, 0])
        self.assertEqual(bp.entities[3], g[5, 5])

    def test_single_1x2(self):
        bp = Blueprint(**BlueprintDict(entities=[
            get_entity_dict("splitter", 1, 0.5),
        ]))
        g = Grid(bp)
        self.assertEqual(2, g.width)
        self.assertEqual(1, g.height)
        self.assertEqual(bp.entities[0], g[0, 0])
        self.assertEqual(bp.entities[0], g[1, 0])

        bp = Blueprint(**BlueprintDict(entities=[
            get_entity_dict("splitter", 0.5, 1, direction=2),
        ]))
        g = Grid(bp)
        self.assertEqual(1, g.width)
        self.assertEqual(2, g.height)
        self.assertEqual(bp.entities[0], g[0, 0])
        self.assertEqual(bp.entities[0], g[0, 1])

        bp = Blueprint(**BlueprintDict(entities=[
            get_entity_dict("splitter", -1, 0.5),
        ]))
        g = Grid(bp)
        self.assertEqual(2, g.width)
        self.assertEqual(1, g.height)
        self.assertEqual(bp.entities[0], g[0, 0])
        self.assertEqual(bp.entities[0], g[1, 0])

    def test_multiple_1x2(self):
        bp = Blueprint(**BlueprintDict(entities=[
            get_entity_dict("splitter", 1, 0.5),
            get_entity_dict("splitter", 1.5, 2, direction=2),
            get_entity_dict("splitter", -0.5, 2),
        ]))
        g = Grid(bp)
        self.assertIsNone(g[0, 0])
        self.assertEqual(bp.entities[0], g[1, 0])
        self.assertEqual(bp.entities[0], g[2, 0])
        self.assertIsNone(g[0, 1])
        self.assertIsNone(g[1, 1])
        self.assertEqual(bp.entities[1], g[2, 1])
        self.assertEqual(bp.entities[2], g[0, 2])
        self.assertEqual(bp.entities[2], g[1, 2])
        self.assertEqual(bp.entities[1], g[2, 2])

    def test_mixed(self):
        bp = Blueprint(**BlueprintDict(entities=[
            get_entity_dict("assembling-machine-1", 9.5, -5.5),
            get_entity_dict("electric-furnace", 6.5, -3.5),
            get_entity_dict("transport-belt", 8.5, -3.5),
            get_entity_dict("splitter", 5.5, -7, direction=2),
        ]))
        g = Grid(bp)
        self.assertEqual(6, g.width)
        self.assertEqual(6, g.height)
        self.assertEqual(g[0, 0], bp.entities[3])
        self.assertEqual(g[0, 1], bp.entities[3])
        self.assertEqual(g[3, 1], bp.entities[0])
        self.assertEqual(g[4, 1], bp.entities[0])
        self.assertEqual(g[5, 1], bp.entities[0])
        self.assertEqual(g[3, 2], bp.entities[0])
        self.assertEqual(g[4, 2], bp.entities[0])
        self.assertEqual(g[5, 2], bp.entities[0])
        self.assertEqual(g[3, 3], bp.entities[0])
        self.assertEqual(g[4, 3], bp.entities[0])
        self.assertEqual(g[5, 3], bp.entities[0])
        self.assertEqual(g[0, 3], bp.entities[1])
        self.assertEqual(g[1, 3], bp.entities[1])
        self.assertEqual(g[2, 3], bp.entities[1])
        self.assertEqual(g[0, 4], bp.entities[1])
        self.assertEqual(g[1, 4], bp.entities[1])
        self.assertEqual(g[2, 4], bp.entities[1])
        self.assertEqual(g[0, 5], bp.entities[1])
        self.assertEqual(g[1, 5], bp.entities[1])
        self.assertEqual(g[2, 5], bp.entities[1])
        self.assertEqual(g[3, 4], bp.entities[2])
