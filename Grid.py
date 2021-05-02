from typing import Tuple

import numpy as np

import blueprintString
from Blueprint.Blueprint import Blueprint, BlueprintDict
from Blueprint.BlueprintWrapper import BlueprintWrapper
from Blueprint.Entity import Entity
from Blueprint.Tests.test_Entity import get_entity_dict


class Grid:
    def __init__(self, blueprint: Blueprint, width=None, height=None, x_offset=None, y_offset=None):
        self.blueprint = blueprint
        low, high = blueprint.bounding_box

        if width is None or height is None:
            self.width, self.height = blueprint.get_dimensions()
        else:
            self.width = width
            self.height = height

        if x_offset is None or y_offset is None:
            self.x_offset = np.floor(low.x)
            self.y_offset = np.floor(low.y)
        else:
            self.x_offset = x_offset
            self.y_offset = y_offset

        self.grid = np.empty(shape=(self.height, self.width), dtype=Entity)
        self._yd, self._xd = np.indices((self.height, self.width))
        self._yd = self._yd + self.y_offset
        self._xd = self._xd + self.x_offset

        for e in blueprint.entities:
            self.add_entity(e)

    def add_entity(self, entity: Entity):
        mask = entity.get_collision_mask()

        bl, tl, br, tr = entity.bounding_box
        x_offset = int(tl[0] - self.x_offset)
        y_offset = int(tl[1] - self.y_offset)

        if np.all(mask):
            self.grid[y_offset: y_offset + mask.shape[0],
                      x_offset: x_offset + mask.shape[1]] = entity
        else:
            obj_mask = np.ma.masked_where(~mask, np.full(mask.shape, entity, dtype=Entity))
            self.grid[y_offset: y_offset + mask.shape[0],
                      x_offset: x_offset + mask.shape[1]][~obj_mask.mask] = np.ma.compressed(obj_mask)

    def __repr__(self):
        lines = []
        for i in range(self.height):
            line = []
            for j in range(self.width):
                e: Entity = self.grid[i][j]
                if e is None:
                    line.append("_")
                    continue
                line.append(e.name[0])

            lines.append("".join(line))
        return "\n".join(lines)

    def __getitem__(self, item: Tuple[int, int]) -> Entity:
        x, y = item
        return self.grid[y][x]


def _main():
    bp = Blueprint(**BlueprintDict(entities=[
        get_entity_dict("transport-belt", -3.5, 0.5),
        get_entity_dict("transport-belt", 2.5, 2.5),
        get_entity_dict("assembling-machine-1", 5.5, 2.5),
        get_entity_dict("splitter", 0.5, 2, direction=2),

    ]))
    print(bp)
    g: Grid = Grid(bp)
    print(g)


if __name__ == '__main__':
    _main()
