from collections import namedtuple
from typing import Union

Point = namedtuple('Point', 'x,y', defaults=[0, 0])
Point3d = namedtuple('Point3d', 'x,y,z', defaults=[0, 0, 0])

DIRECT_ADJACENTS = ((0, -1), (-1, 0), (1, 0), (0, 1))  # 4 adjacent nodes
ALL_ADJACENTS = ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))

NORTH = Point(0, -1)
EAST = Point(1, 0)
SOUTH = Point(0, 1)
WEST = Point(-1, 0)


def translate(p: Union[Point, Point3d, tuple], offset: tuple) -> Union[Point, Point3d, tuple]:
    if type(p) == Point:
        return Point(p.x + offset[0], p.y + offset[1])
    if type(p) == Point3d:
        return Point3d(p.x + offset[0], p.y + offset[1], p.z + offset[2])
    if type(p) == tuple:
        assert len(p) == len(offset)
        result = []
        for i in range(len(p)):
            result.append(p[i] + offset[i])
        return tuple(result)
    raise ValueError(f'can not translate {type(p)}')


def rot_cw(p: tuple) -> tuple:
    return Point(-p[1], p[0])


def rot_ccw(p: tuple) -> tuple:
    return Point(p[1], -p[0])

def length(p) -> int:
    return sum(map(abs,p))

def manhattan_distance(p1, p2) -> int:
    assert len(p1) == len(p2)
    ans = 0
    for i in range(len(p1)):
        ans += abs(p1[i]-p2[i])
    return ans


def all_adjacent_iter(p: tuple, width: int = 0, height: int = 0):
    yield from _adjacent_iter(p, width, height)


def direct_adjacent_iter(p: tuple, width: int = 0, height: int = 0):
    yield from _adjacent_iter(p, width, height, DIRECT_ADJACENTS)


def _adjacent_iter(p: tuple, width: int = 0, height: int = 0, adjacents=ALL_ADJACENTS):
    for dx, dy in adjacents:
        np = Point(p[0] + dx, p[1] + dy)
        if width > 0 and (np.x < 0 or np.x >= width):
            continue
        if height > 0 and (np.y < 0 or np.y >= height):
            continue
        yield np

def point_by_row(self, other):
    if self[1] == other[1]:
        return self[0]-other[0]
    else:
        return self[1]-other[1]
