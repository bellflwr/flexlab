from math import cos, radians

SIN_30 = 0.5
# COS_30 = 181 / 209
# COS_30 = 6/7
COS_30 = 0.866025403784438646763723170752936183471


def ceildiv(a, b):
    return -(a // -b)


def get_triangle_coordinates(x: int, y: int, side_length: float) -> tuple[
    tuple[float, float], tuple[float, float], tuple[float, float]]:
    even_x = x % 2 == 0
    even_y = y % 2 == 0

    x_spacing = SIN_30 * side_length
    y_spacing = COS_30 * side_length

    if even_y:
        ax = side_length * ceildiv(x, 2)
    else:
        ax = side_length * (x // 2 + SIN_30)

    ay = y * y_spacing

    if even_x == even_y:
        bx = ax + side_length
        by = ay
    else:
        bx = ax + x_spacing
        by = ay + y_spacing

    if even_x == even_y:
        cx = ax + x_spacing
    else:
        cx = ax - x_spacing

    cy = ay + y_spacing

    return (ax, ay), (bx, by), (cx, cy)


def fuck(x, y):
    return x % 4 == 1 and y % 4 in (0, 3) or \
           x % 4 == 3 and y % 4 in (2, 1)
