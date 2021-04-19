import json
from typing import Generator, Tuple, Iterable, Dict

import numpy as np
from typing_extensions import TypedDict

import blueprintString
from Blueprint.Blueprint import Blueprint
from Blueprint.BlueprintWrapper import BlueprintWrapper, BlueprintWrapperDict
from Blueprint.Entity import Entity
from Blueprint.Exceptions.UnknownEntityException import UnknownEntityException
from Grid import Grid
from data import iter_stored_blueprints, load_blueprints


def iter_individual_blueprints(verbose: False) -> Generator[Tuple[str, Blueprint], None, None]:
    # passed = 0
    for k, bpDict in iter_stored_blueprints():
        # if k == "-MK87s2dm3zOKGYlwaVl":
        #     passed = 1
        #     print("passed")
        # if passed == 0:
        #     continue
        # print(k)
        try:
            wrapper = BlueprintWrapper(**bpDict)
        except KeyError:
            continue
        except UnknownEntityException as e:
            if verbose:
                print(f"Uknown entity in {k}: {e}")
            continue
        except Exception as e:
            raise Exception(f"Error processing blueprint with key {k}.") from e

        for bp in wrapper.iter_items():
            yield k, bp


def one_hot_encode_grid(grid: Grid, entity_index_map: Dict[str, int]):
    (l, w) = grid.grid.shape
    one_hot_grid = np.zeros((l, w, len(entity_index_map)), dtype=int)

    for i in range(len(grid.grid)):
        for j in range(len(grid.grid[0])):
            entity: Entity = grid.grid[i][j]
            if entity is None:
                continue

            one_hot_grid[i][j][entity_index_map[entity.name]] = 1
    return one_hot_grid


def lookup(e: Entity):
    if e is None or e.name not in entity_index_map:
        return -1, False
    return entity_index_map[e.name], True


def one_hot_encode_grid_vec(grid: Grid, entity_index_map: Dict[str, int]):
    encoding_size = len(entity_index_map)
    out = np.zeros((grid.grid.size, encoding_size), dtype=bool)

    a, b = vf(grid.grid)

    out[np.arange(a.size), np.ravel(a)] = np.ravel(b)
    out = out.reshape(grid.grid.shape + (encoding_size,))
    return out


def grid_entities():
    iterator = iter_individual_blueprints()

    for i, (k, bp) in enumerate(iterator):
        g = Grid(bp)
        encoding = one_hot_encode_grid_vec(g, entity_index_map)


def fill_entity_dict():
    entity_index_map = {}

    index = 0
    for k in Entity.get_entity_size_dict().keys():
        if not str(k).endswith("remnants"):
            entity_index_map[str(k)] = index
            index += 1

    return entity_index_map


vf = np.vectorize(lookup, otypes=[int, bool])
entity_index_map = fill_entity_dict()
grid_entities()




