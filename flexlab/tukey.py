# from __future__ import annotations
from itertools import product
from typing import TypeAlias
from collections.abc import Iterable, Iterator

Tukey: TypeAlias = "tuple[Tukey, Tukey] | None"


def _parse_tukey(itr: Iterator[str]) -> Tukey:
    a = _parse_tukey(itr) if next(itr) == "+" else None
    b = _parse_tukey(itr) if next(itr) == "+" else None

    return a, b


def parse_tukey(inp: Iterable[str]) -> Tukey:
    itr = iter(inp)
    try:
        return _parse_tukey(itr)
    except StopIteration:
        raise SyntaxError("Tree was never closed")


def count_units(tk: Tukey) -> int:
    if tk is None:
        return 0

    count = 1

    count += count_units(tk[0])
    count += count_units(tk[1])

    return count


def add_tuple(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return a[0] + b[0], a[1] + b[1]


def rotate(a: tuple[int, int], right: bool) -> tuple[int, int]:
    if not right:
        return -a[1], a[0]
    return a[1], -a[0]


def invert(a: tuple[int, int]) -> tuple[int, int]:
    return -a[0], -a[1]


UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def create_grid(otk: Tukey) -> list[list[bool | None]]:
    grid: list[list[bool | None]] = [[None for _ in range(6)] for _ in range(6)]

    def confuse(tk, pos, dfrom, *, first=False):
        grid[pos[1]][pos[0]] = first

        if tk is None:
            return 

        if pos[0] % 2 == pos[1] % 2:
            if dfrom == LEFT:
                l = UP
                r = RIGHT
            elif dfrom == UP:
                l = RIGHT
                r = LEFT
            elif dfrom == RIGHT:
                l = LEFT
                r = UP
        else:
            if dfrom == LEFT:
                l = RIGHT
                r = DOWN
            elif dfrom == DOWN:
                l = LEFT
                r = RIGHT
            elif dfrom == RIGHT:
                l = DOWN
                r = LEFT

        if tk[0] is not None:
            new_pos = add_tuple(pos, l)
            confuse(tk[0], new_pos, invert(l))

        if tk[1] is not None:
            new_pos = add_tuple(pos, r)
            confuse(tk[0], new_pos, invert(r))

    confuse(otk, (2, 2), dfrom=LEFT, first=True)

    return grid


# surfaces = 6
# units = surfaces - 2
#
#
# slay = []
#
# for i in map("".join, product("+.", repeat=units*2)):
#     try:
#         t = parse_tukey(i)
#     except SyntaxError:
#         continue
#
#     if count_units(t) == units:
#
#         slay.append((i, t))
#
# for s in slay:
#     print(*s)
