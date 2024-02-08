# from __future__ import annotations
from itertools import product
from typing import TypeAlias, TypeVar, Generic
from collections.abc import Iterable, Iterator, Generator
from rich import print
from rich.pretty import pprint

T = TypeVar("T")

IVector: TypeAlias = tuple[int, int]

BinTree: TypeAlias = "tuple[BinTree, BinTree] | None"
DataBinTree: TypeAlias = "tuple[T, DataBinTree, DataBinTree] | None"

Tukey: TypeAlias = BinTree
DisplaceTree: TypeAlias = "DataBinTree[IVector]"


def _parse_tukey(itr: Iterator[str]) -> Tukey:
    a = _parse_tukey(itr) if next(itr) == "+" else None
    b = _parse_tukey(itr) if next(itr) == "+" else None

    return a, b


def parse_tukey(inp: Iterable[str]) -> Tukey:
    itr = iter(inp)
    try:
        tk = _parse_tukey(itr)
    except StopIteration:
        raise SyntaxError("Tree was never closed")

    try:
        next(itr)
    except StopIteration:
        return tk

    raise SyntaxError("Unexpected character after tree was formed")

def _encode_tukey(tk: Tukey) -> str:
    if tk is None:
        return "."

    return "+" + _encode_tukey(tk[0]) + _encode_tukey(tk[1])


def encode_tukey(tk: Tukey) -> str:
    return _encode_tukey(tk[0]) + _encode_tukey(tk[1])




def render_tree(tk: Tukey) -> str:
    if tk is None:
        return "."

    else:
        return "({} {})".format(render_tree(tk[0]), render_tree(tk[1]))


def count_units(tk: Tukey) -> int:
    if tk is None:
        return 0

    count = 1

    count += count_units(tk[0])
    count += count_units(tk[1])

    return count


def add_tuple(a: IVector, b: IVector) -> IVector:
    return a[0] + b[0], a[1] + b[1]


def rotate(a: IVector, right: bool) -> IVector:
    if not right:
        return -a[1], a[0]
    return a[1], -a[0]


def invert(a: IVector) -> IVector:
    return -a[0], -a[1]


UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def get_relative_displacement(last_dis: IVector, last_t_up: bool) -> tuple[IVector, IVector]:
    if last_t_up:
        if last_dis == RIGHT:
            return UP, RIGHT
        elif last_dis == DOWN:
            return RIGHT, LEFT
        elif last_dis == LEFT:
            return LEFT, UP
    else:
        if last_dis == RIGHT:
            return RIGHT, DOWN
        elif last_dis == UP:
            return LEFT, RIGHT
        elif last_dis == LEFT:
            return DOWN, LEFT


def create_displacement_tree(tk: Tukey, pos: IVector = (0, 0), last_dis: IVector = RIGHT) -> DisplaceTree:
    l, r = None, None

    last_t_up = pos[0] % 2 != pos[1] % 2
    l_dis, r_dis = get_relative_displacement(last_dis, last_t_up)

    if tk[0] is not None:
        l = create_displacement_tree(tk[0], add_tuple(pos, l_dis), l_dis)

    if tk[1] is not None:
        r = create_displacement_tree(tk[1], add_tuple(pos, r_dis), r_dis)

    return l_dis, l, r


def render_displacement_tree(dt: DisplaceTree) -> str:
    txt = str(dt[0])
    txt += "\n"
    txt += "Left:"
    txt += "\n"
    if dt[1] is not None:
        txt += "\t" + render_displacement_tree(dt[1]).replace("\n", "\n\t")
    txt += "\n"
    txt += "Right:"
    txt += "\n"

    if dt[2] is not None:
        txt += "\t" + render_displacement_tree(dt[2]).replace("\n", "\n\t")
    txt += "\n"

    return txt


def create_grid(dis_tree: DisplaceTree) -> list[list[bool | None]]:
    grid: list[list[bool | None]] = [[None for _ in range(10)] for _ in range(10)]

    def traverse(pos, dt, first=False):
        new_pos = add_tuple(pos, dt[0])
        grid[new_pos[1]][new_pos[0]] = first

        if dt[1] is not None:
            traverse(new_pos, dt[1])

        if dt[2] is not None:
            traverse(new_pos, dt[2])

    traverse((3, 2), dis_tree, True)

    return grid


def create_grid_from_tukey(tk: Tukey) -> list[list[bool | None]]:
    return create_grid(create_displacement_tree(tk))


def normalize_tukey(tk: Tukey) -> Tukey:
    if tk is None:
        return tk

    l = normalize_tukey(tk[0])
    r = normalize_tukey(tk[1])

    if count_units(l) < count_units(r):
        return r, l

    return l, r


def is_normalized(tk: Tukey) -> bool:
    return tk == normalize_tukey(tk)


def generate_all_tukeys(surfaces: int) -> Generator[str, None, None]:
    units = surfaces - 2

    for i in map("".join, product("+.", repeat=units * 2)):
        try:
            t = parse_tukey(i)
        except SyntaxError:
            continue

        if encode_tukey(t) != i:
            print(f"{i} != {t}")

        if count_units(t) != units:
            continue

        if t[1] is not None:
            continue

        # if not is_normalized(t):
        #     continue

        if count_units(t[0][0]) < count_units(t[0][1]):
            continue


        yield i
