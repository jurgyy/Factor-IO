import copy
import random
from typing import Tuple, Generator, Dict
import numpy as np

from Blueprint.Blueprint import Blueprint
from Blueprint.BlueprintWrapper import BlueprintWrapper
from Blueprint.Entity import Entity
from Blueprint.Exceptions.UnknownEntityException import UnknownEntityException
from Grid import Grid
from data import iter_stored_blueprints


# TODO remove
np.set_printoptions(edgeitems=1000, linewidth=1000)


class TrainGenerator:
    def __init__(self, minimum_entity_count: int = 3, train_omission_portion: float = 0.1, seed: int = None, verbose: bool = False):
        self.chunk_size: int = 32
        self.step_size: int = 16
        self.minimum_entity_count: int = minimum_entity_count

        if not 0 < train_omission_portion < 1.:
            raise Exception("train_omission_portion should be between 0 and 1")
        self.train_omission_portion: float = train_omission_portion
        self.seed: int = seed
        random.seed = self.seed
        self.verbose: bool = verbose

        self.entity_index_map, self.reverse_entity_index_map = self._get_entity_index_dicts()
        self._e_lookup = np.vectorize(TrainGenerator._lookup_entity_index, otypes=[int, bool])
        self._re_lookup = np.vectorize(TrainGenerator._reverse_lookup_entity_index, otypes=[str])


    def _validate_entity_array(self, entity_array: np.array) -> bool:
        # TODO check number of entities?
        return True

    @staticmethod
    def _get_entity_index_dicts() -> Tuple[dict, dict]:
        entity_index_map = {}
        reverse_index_map = {}

        index = 0
        for k in Entity.get_entity_size_dict().keys():
            if not str(k).endswith("remnants"):
                entity_index_map[str(k)] = index
                reverse_index_map[index] = str(k)
                index += 1

        return entity_index_map, reverse_index_map

    @staticmethod
    def _lookup_entity_index(e: Entity, entity_index_map: Dict[str, int]):
        if e is None or e.name not in entity_index_map:
            return -1, False
        return entity_index_map[e.name], True

    @staticmethod
    def _reverse_lookup_entity_index(index: int, reverse_entity_index_map: Dict[int, str]):
        if index not in reverse_entity_index_map:
            return None
        return reverse_entity_index_map[index]

    def one_hot_encode_grid(self, entity_array: np.array) -> np.array:
        (h, w) = entity_array.shape
        one_hot_grid = np.zeros((h, w, len(self.entity_index_map)), dtype=int)

        for i in range(h):
            for j in range(w):
                entity: Entity = entity_array[i][j]
                if entity is None:
                    continue

                one_hot_grid[i][j][self.entity_index_map[entity.name]] = 1
        return one_hot_grid

    def one_hot_decode_grid(self, one_hot_grid: np.array) -> np.array:
        # if all zero set the value of the cell to -1 else set to the argmax (index of max value)
        amax = np.where(np.count_nonzero(one_hot_grid, axis=-1) == 0,
                        -1,
                        np.argmax(one_hot_grid, axis=-1))
        return self._re_lookup(amax, self.reverse_entity_index_map)

    @staticmethod
    def _tile_numpy(grid_array: np.array, size: Tuple[int, int], border: int = 1) -> np.array:
        a = np.zeros((grid_array.shape[0] + border,
                      grid_array.shape[1] + border,
                      grid_array.shape[2]))
        a[: grid_array.shape[0], :grid_array.shape[1], :grid_array.shape[2]] = grid_array

        xn = int(np.ceil(size[1] / a.shape[1]))
        yn = int(np.ceil(size[0] / a.shape[0]))

        a = np.tile(a, [yn, xn, 1])
        return a[:size[0], :size[1]]

    def iter_grid_chunks(self, img: np.array) -> Generator[np.array, None, None]:
        if self.chunk_size % self.step_size != 0 or self.step_size > self.chunk_size:
            # Ensure size is a multiple of the step size
            raise Exception("Chunk size should be a larger multiple of step size in both dimensions")

        size = (int(np.ceil(img.shape[0] / self.step_size)) * self.step_size,
                int(np.ceil(img.shape[1] / self.step_size)) * self.step_size)

        tiled_img = self._tile_numpy(img, size)

        xs = np.arange(0, tiled_img.shape[1] - self.step_size, self.step_size)
        ys = np.arange(0, tiled_img.shape[0] - self.step_size, self.step_size)
        for x in xs:
            for y in ys:
                yield tiled_img[y: y + self.chunk_size, x: x + self.chunk_size]

    def iter_individual_blueprints(self) -> Generator[Blueprint, None, None]:
        for k, bpDict in iter_stored_blueprints(self.seed):
            try:
                wrapper = BlueprintWrapper(**bpDict)
            except KeyError as e:
                if self.verbose:
                    print(e)
                continue
            except UnknownEntityException as e:
                if self.verbose:
                    print(f"Unknown entity in {k}: {e}")
                continue
            except Exception:
                if self.verbose:
                    print(f"Error processing blueprint with key {k}.")
                continue

            for bp in wrapper.iter_items():
                yield bp

    def iter_training_set(self) -> Generator[Tuple[np.array, np.array], None, None]:
        for bp in self.iter_individual_blueprints():
            omit_bp = copy.deepcopy(bp)
            omit_bp.entities = omit_bp.entities[int(self.train_omission_portion * len(bp.entities)):]

            grid = Grid(bp)
            self._validate_entity_array(grid.grid)

            omit_grid = Grid(omit_bp, grid.width, grid.height, grid.x_offset, grid.y_offset)

            one_hot = self.one_hot_encode_grid(grid.grid)
            omit_one_hot = self.one_hot_encode_grid(omit_grid.grid)
            for x, y in zip(self.iter_grid_chunks(omit_one_hot), self.iter_grid_chunks(one_hot)):
                s = np.sum(y)
                if s - s * self.train_omission_portion < self.minimum_entity_count:
                    continue

                yield x, y


def main():
    import time

    gen = TrainGenerator(seed=None, verbose=True)

    t0 = time.time()
    for i, (x, y) in enumerate(gen.iter_training_set()):
        if i > 1000:
            break
        # print(gen.one_hot_decode_grid(x))
    t1 = time.time()
    print(t1 - t0)


if __name__ == '__main__':
    main()
