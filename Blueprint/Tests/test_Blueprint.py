from unittest import TestCase

from Blueprint.Blueprint import BlueprintDict, Blueprint
from Blueprint.Position import Position
from Blueprint.Tests.test_Entity import get_entity_dict


class TestBlueprint(TestCase):
    def test_get_dimensions_single_1x1(self):
        bp = Blueprint(**BlueprintDict(entities=[get_entity_dict("transport-belt", 0.5, 0.5)]))
        self.assertEqual((1, 1), bp.get_dimensions())

    def test_get_dimensions_single_3x3(self):
        bp = Blueprint(**BlueprintDict(entities=[get_entity_dict("assembling-machine-1", 1.5, 1.5)]))
        self.assertEqual((3, 3), bp.get_dimensions())

    def test_bounding_box_single_1x1(self):
        bp = Blueprint(**BlueprintDict(entities=[get_entity_dict("transport-belt", 0.5, 0.5)]))
        self.assertEqual((Position(0, 0), Position(1, 1)), bp.bounding_box)

        bp = Blueprint(**BlueprintDict(entities=[get_entity_dict("transport-belt", -0.5, -0.5)]))
        self.assertEqual((Position(-1, -1), Position(0, 0)), bp.bounding_box)

    def test_bounding_box_single_3x3(self):
        bp = Blueprint(**BlueprintDict(entities=[get_entity_dict("assembling-machine-1", 0.5, 0.5)]))
        self.assertEqual((Position(-1, -1), Position(2, 2)), bp.bounding_box)

        bp = Blueprint(**BlueprintDict(entities=[get_entity_dict("assembling-machine-1", 1.5, 1.5)]))
        self.assertEqual((Position(0, 0), Position(3, 3)), bp.bounding_box)

        bp = Blueprint(**BlueprintDict(entities=[get_entity_dict("assembling-machine-1", -1.5, -1.5)]))
        self.assertEqual((Position(-3, -3), Position(0, 0)), bp.bounding_box)

    def test_get_dimensions_3x3_square(self):
        bp = Blueprint(**BlueprintDict(entities=[
            get_entity_dict("transport-belt", 0.5, 0.5),
            get_entity_dict("transport-belt", 2.5, 2.5),
        ]))
        self.assertEqual((3, 3), bp.get_dimensions())

        bp = Blueprint(**BlueprintDict(entities=[
            get_entity_dict("assembling-machine-1", -0.5, -0.5),
            get_entity_dict("transport-belt", 2.5, 2.5),
        ]))
        self.assertEqual((5, 5), bp.get_dimensions())

    def test_get_dimensions_mixed(self):
        bp = Blueprint(**BlueprintDict(entities=[
            get_entity_dict("stone-furnace", -10, 0),
            get_entity_dict("stone-furnace", 10, 0),
        ]))
        self.assertEqual((22, 2), bp.get_dimensions())

    def test_get_dimensions_single_rails(self):
        bp = Blueprint(**BlueprintDict(entities=[
            get_entity_dict("curved-rail", 0, 0)
        ]))
        self.assertEqual((5, 8), bp.get_dimensions())

        bp = Blueprint(**BlueprintDict(entities=[
            get_entity_dict("curved-rail", 0, 0, direction=5)
        ]))
        self.assertEqual((5, 8), bp.get_dimensions())

        bp = Blueprint(**BlueprintDict(entities=[
            get_entity_dict("curved-rail", 0, 0, direction=2)
        ]))
        self.assertEqual((8, 5), bp.get_dimensions())

    def test_get_dimensions_multiple_rails(self):
        bp = Blueprint(**BlueprintDict(entities=[
            get_entity_dict("curved-rail", 0, 0),
            get_entity_dict("curved-rail", 18, 0)
        ]))
        self.assertEqual((23, 8), bp.get_dimensions())

        bp = Blueprint(**BlueprintDict(entities=[
            get_entity_dict("curved-rail", 0, 0, direction=0),
            get_entity_dict("curved-rail", 18, 0, direction=4)
        ]))
        self.assertEqual((24, 8), bp.get_dimensions())

        bp = Blueprint(**BlueprintDict(entities=[
            get_entity_dict("curved-rail", 0, 0, direction=2),
            get_entity_dict("curved-rail", 0, 18, direction=2)
        ]))
        self.assertEqual((8, 23), bp.get_dimensions())

        bp = Blueprint(**BlueprintDict(entities=[
            get_entity_dict("curved-rail", 0, 0, direction=2),
            get_entity_dict("curved-rail", 0, 18, direction=6)
        ]))
        self.assertEqual((8, 24), bp.get_dimensions())

    def test_get_bounding_box_3x3_square(self):
        bp = Blueprint(**BlueprintDict(entities=[
            get_entity_dict("transport-belt", 0.5, 0.5),
            get_entity_dict("transport-belt", 2.5, 2.5),
        ]))
        self.assertEqual((Position(0, 0), Position(3, 3)), bp.bounding_box)

        bp = Blueprint(**BlueprintDict(entities=[
            get_entity_dict("transport-belt", -0.5, -0.5),
            get_entity_dict("transport-belt", 1.5, 1.5),
        ]))
        self.assertEqual((Position(-1, -1), Position(2, 2)), bp.bounding_box)

        bp = Blueprint(**BlueprintDict(entities=[
            get_entity_dict("transport-belt", -2.5, -2.5),
            get_entity_dict("transport-belt", -0.5, -0.5),
        ]))
        self.assertEqual((Position(-3, -3), Position(0, 0)), bp.bounding_box)
