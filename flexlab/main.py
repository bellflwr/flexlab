from itertools import product

import dearpygui.dearpygui as dpg

from flexlab.tukey import create_grid, create_displacement_tree, parse_tukey, render_tree, generate_all_tukeys, \
    render_displacement_tree
from mathutil import get_triangle_coordinates, fuck, COS_30
import json

from pprint import pformat

VP_SIZE = 10, 10

SIX_1 = [
    '++..+...',
    '.++..+..'
]

SIX_2 = [
    '+++.....',
    '+.+.+...',
    '+.+..+..',
    '+..++...',
    '.+++....',
    '.+.+.+..'
]

SIX_3 = [
    '++.+....'
    '++...+..'
    '+.++....'
    '+..+.+..'
    '.++.+...'
    '.+.++...'
]


def update_diagram():
    dpg.delete_item("Tukey Diagram", children_only=True)

    for x, y in product(range(VP_SIZE[0] * 2 + 1), range(VP_SIZE[1] * 2)):
        a, b, c = get_triangle_coordinates(x, y, 50)
        dpg.draw_triangle(a, b, c, color=(100, 100, 100), parent="Tukey Diagram")

    # for x, y in product(range(8), range(8)):
    #
    #     if fuck(x, y):
    #
    #         a, b, c = get_triangle_coordinates(x, y, 50)
    #         dpg.draw_triangle(a, b, c)

    tk = parse_tukey(dpg.get_value("Tukey Input"))
    dt = create_displacement_tree(tk)

    dpg.set_value("Tukey Tree", render_tree(tk))
    dpg.set_value("Displacement Tree", render_displacement_tree(dt))

    joil = create_grid(dt)

    for y, row in enumerate(joil):
        for x, cell in enumerate(row):
            if cell is not None:
                color = (0, 255, 0) if cell else (255, 0, 0)
                a, b, c = get_triangle_coordinates(x, y, 100)
                dpg.draw_triangle(a, b, c, color=color, parent="Tukey Diagram")


def print_diagram():
    print(repr(dpg.get_value("Tukey Input")))

def normalize_diagram():
    pass

def save_layout():
    dpg.save_init_file("dpg.ini")


def main():
    dpg.create_context()

    with dpg.font_registry():
        default_font = dpg.add_font("flexlab/assets/fonts/InterVariable.ttf", 20)

    dpg.create_viewport(title='Custom Title')

    dpg.configure_app(docking=True, docking_space=True, init_file="dpg.ini")

    dpg.bind_font(default_font)

    with dpg.viewport_menu_bar():
        with dpg.menu(label="View"):
            dpg.add_menu_item(label="Save Layout", callback=save_layout)

    with dpg.window(label="Tukey Viewport", tag="Tukey Viewport", horizontal_scrollbar=True, autosize=True):
        dw = dpg.add_drawlist(VP_SIZE[0] * 100, VP_SIZE[1] * 100 * COS_30, tag="Tukey Diagram")

    with dpg.window(label="Primary Window", tag="Primary Window"):
        com = dpg.add_combo(
            items=tuple(generate_all_tukeys(7)),
            # items=SIX_2,
            callback=update_diagram
        )
        inp = dpg.add_input_text(default_value="++....", tag="Tukey Input", source=com, callback=update_diagram)
        dpg.add_button(label="Render", callback=update_diagram)
        dpg.add_button(label="Print", callback=print_diagram)
        dpg.add_button(label="Normalize", callback=normalize_diagram)
        dpg.add_text(tag="Tukey Tree")
        dpg.add_text(tag="Displacement Tree")

    dpg.setup_dearpygui()
    # dpg.show_item_registry()
    dpg.show_viewport()
    dpg.maximize_viewport()
    dpg.start_dearpygui()

    dpg.destroy_context()


if __name__ == "__main__":
    main()
