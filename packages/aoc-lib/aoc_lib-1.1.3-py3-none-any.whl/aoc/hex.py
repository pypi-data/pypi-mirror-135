from __future__ import nested_scopes
from __future__ import division


class Hex:
    def __init__(self, q, r, s):
        assert (round(q + r + s) == 0), "q + r + s must be 0"
        self.q = q
        self.r = r
        self.s = s

    def __eq__(self, other):
        return self.q == other.q and self.r == other.r and self.s == other.s

    def __sub__(self, other):
        return Hex(self.q - other.q, self.r - other.r, self.s - other.s)

    def __add__(self, other):
        return Hex(self.q + other.q, self.r + other.r, self.s + other.s)

    def __mul__(self, k):
        return Hex(self.q * k, self.r * k, self.s * k)

    def __str__(self):
        return f"({self.q},{self.r},{self.s})"

    def rotate_left(self):
        return Hex(-self.s, -self.q, -self.r)

    def rotate_right(self):
        return Hex(-self.r, -self.s, -self.q)

    def direction(self, dir):
        return HEX_DIRECTIONS[dir] if type(dir) == int else HEX_NAMED_DIRECTIONS[dir]

    def neighbor(self, dir):
        return self + self.direction(dir)

    def diagonal_neighbor(self, dir):
        return self + HEX_DIAGONALS[dir]

    def length(self):
        return (abs(self.q) + abs(self.r) + abs(self.s)) // 2

    def distance(self, b):
        return (self - b).length()

    def round(self):
        qi = int(round(self.q))
        ri = int(round(self.r))
        si = int(round(self.s))
        q_diff = abs(qi - self.q)
        r_diff = abs(ri - self.r)
        s_diff = abs(si - self.s)
        if q_diff > r_diff and q_diff > s_diff:
            qi = -ri - si
        else:
            if r_diff > s_diff:
                ri = -qi - si
            else:
                si = -qi - ri
        return Hex(qi, ri, si)

    def lerp(self, b, t):
        return Hex(self.q * (1.0 - t) + b.q * t, self.r * (1.0 - t) + b.r * t, self.s * (1.0 - t) + b.s * t)

    def linedraw(self, b):
        N = self.distance(b)
        a_nudge = Hex(self.q + 1e-06, self.r + 1e-06, self.s - 2e-06)
        b_nudge = Hex(b.q + 1e-06, b.r + 1e-06, b.s - 2e-06)
        results = []
        step = 1.0 / max(N, 1)
        for i in range(0, N + 1):
            results.append(a_nudge.lerp(b_nudge, step * i).round())
        return results


HEX_DIRECTIONS = [Hex(1, 0, -1), Hex(1, -1, 0), Hex(0, -1, 1), Hex(-1, 0, 1), Hex(-1, 1, 0), Hex(0, 1, -1)]
HEX_NAMED_DIRECTIONS = {'n': Hex(0, -1, 1), 'ne': Hex(1, -1, 0), 'se': Hex(1, 0, -1), 's': Hex(0, 1, -1), 'sw': Hex(-1, 1, 0),
                        'nw': Hex(-1, 0, 1)}
HEX_DIAGONALS = [Hex(2, -1, -1), Hex(1, -2, 1), Hex(-1, -1, 2), Hex(-2, 1, 1), Hex(-1, 2, -1), Hex(1, 1, -2)]
