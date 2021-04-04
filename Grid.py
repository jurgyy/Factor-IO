from typing import Tuple

import numpy as np

from Blueprint.Blueprint import Blueprint, BlueprintDict
from Blueprint.Entity import Entity
from Blueprint.Tests.test_Entity import get_entity_dict


class Grid:
    def __init__(self, blueprint: Blueprint):
        self.blueprint = blueprint
        low, high = blueprint.bounding_box

        self.width: int = int(np.ceil(high.x) - np.floor(low.x))
        self.height: int = int(np.ceil(high.y) - np.floor(low.y))

        self.x_offset = np.floor(low.x)
        self.y_offset = np.floor(low.y)

        self.grid = np.empty(shape=(self.height, self.width), dtype=Entity)
        self._yd, self._xd = np.indices((self.height, self.width))
        self._yd = self._yd + self.y_offset
        self._xd = self._xd + self.x_offset

        for e in blueprint.entities:
            self.add_entity(e)

    def add_entity(self, entity: Entity):
        bl, tl, br, tr = entity.bounding_box

        self.grid[(self._xd >= bl[0]) &
                  (self._xd < tr[0]) &
                  (self._yd >= bl[1]) &
                  (self._yd < tr[1])] = entity

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

    def __getitem__(self, item: Tuple[int, int]):
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