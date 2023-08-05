from dataclasses import dataclass
from typing import Union

from aoc import Point


@dataclass
class Rect:
    """
    Rect class (x,y) with width and height all inclusive
    """
    x: int = 0
    y: int = 0
    w: int = 0
    h: int = 0

    @classmethod
    def boundary(cls, points):
        boundary = None
        for p in points:
            if boundary is None:
                boundary = Rect(*p, 1, 1)
            else:
                boundary.extend(*p)
        return boundary

    def grow(self, i):
        """
        Grows this rectangle by i in all dimensions (x-i,y-i,w+2*i,h+2*i).
        Note that negative amount will shrink the rect.
        :param i: Amount to grow in all dimensions
        :return: the rect itself
        :raises ValueError: if the resulting rect would have negative width or height
        """
        new_width = self.w + (i << 1)
        new_height = self.h + (i << 1)
        if new_width < 0 or new_height < 0:
            raise ValueError(f'shrinked rectangle below zero ({new_width}, {new_height})')

        self.x -= i
        self.y -= i
        self.w = new_width
        self.h = new_height
        return self

    def extend(self, x: Union[tuple,Point,int], y=None):
        """
        Extend the rect to also contain the given point
        :param x: the point or tuple (x,y) to include or the x coordinate
        :param y: y coordinate if p is not tuple or point
        :return: the rect itself for further concatenation
        """
        if type(x) != int:
            x, y = p
        if x < self.x:
            self.w = self.w + self.x - x
            self.x = x
        elif x > self.x + self.w:
            self.w = x - self.x + 1
        if y < self.y:
            self.h = self.h + self.y - y
            self.y = y
        elif y > self.y + self.h:
            self.h = y - self.y + 1
        return self

    def __contains__(self, other):
        if type(other) == Rect:
            return self.x <= other.x and self.y <= other.y and self.x + self.w >= other.x + other.w and self.y + self.h >= other.y + other.h and self.x + self.w > other.x and self.y + self.h > other.y
        return self.x <= other[0] < self.x + self.w and self.y <= other[1] < self.y + self.h

    def __iter__(self):
        for y in range(self.y, self.y + self.h):
            for x in range(self.x, self.x + self.w):
                yield Point(x, y)

    def intersection(self, other):
        x = y = w = h = None

        # Left
        if other.x <= self.x < other.x + other.w:
            x = self.x
        elif self.x <= other.x < self.x + self.w:
            x = other.x
        else:
            return None

        # Right
        if self.x + self.w > other.x and self.x + self.w <= other.x + other.w:
            w = self.x + self.w - x
        elif other.x + other.w > self.x and other.x + other.w <= self.x + self.w:
            w = other.x + other.w - x
        else:
            return None

        # Top
        if self.y >= other.y and self.y < other.y + other.h:
            y = self.y
        elif other.y >= self.y and other.y < self.y + self.h:
            y = other.y
        else:
            return None

        # Bottom
        if self.y + self.h > other.y and self.y + self.h <= other.y + other.h:
            h = self.y + self.h - y
        elif other.y + other.h > self.y and other.y + other.h <= self.y + self.h:
            h = other.y + other.h - y
        else:
            return None
        return Rect(x, y, w, h)
