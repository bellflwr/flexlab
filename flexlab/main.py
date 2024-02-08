from itertools import product

import dearpygui.dearpygui as dpg

from flexlab.tukey import create_grid, parse_tukey, render_tree
from mathutil import get_triangle_coordinates, fuck




def update_diagram(sender, app_data, user_data):
    print(sender)
    print(app_data)
    print(user_data)

    dpg.delete_item("Tukey Diagram", children_only=True)

    # for i in dpg.get_item_children(user_data[0]):
    #     print(i)
        # dpg.delete_item(i)

    for x, y in product(range(40), range(20)):
        a, b, c = get_triangle_coordinates(x, y, 50)
        dpg.draw_triangle(a, b, c, color=(100, 100, 100), parent="Tukey Diagram")


    # for x, y in product(range(8), range(8)):
    #
    #     if fuck(x, y):
    #
    #         a, b, c = get_triangle_coordinates(x, y, 50)
    #         dpg.draw_triangle(a, b, c)

    tk = parse_tukey(dpg.get_value("Tukey Input"))

    dpg.set_value("Tukey Tree", render_tree(tk))

    print(tk)
    joil = create_grid(tk)

    for y, row in enumerate(joil):
        for x, cell in enumerate(row):
            if cell is not None:
                a, b, c = get_triangle_coordinates(x, y, 100)
                dpg.draw_triangle(a, b, c, color=(255, 0, 0), parent="Tukey Diagram")




def main():
    dpg.create_context()

    with dpg.font_registry():
        default_font = dpg.add_font("flexlab/assets/fonts/InterVariable.ttf", 20)

    dpg.create_viewport(title='Custom Title')

    dpg.configure_app(docking=True, docking_space=True)

    dpg.bind_font(default_font)

    with dpg.window(label="Tukey Viewport", tag="Tukey Viewport", horizontal_scrollbar=True, autosize=True):
        # for k, v in dpg.get_item_configuration("Tukey Viewport").items():
        #     print(f"{k:>20}: {repr(v)}")
        print(dpg.get_item_width("Tukey Viewport"), dpg.get_item_height("Tukey Viewport"))
        dw = dpg.add_drawlist(1000, 1000, tag="Tukey Diagram")



    with dpg.window(label="Primary Window", tag="Primary Window"):
        inp = dpg.add_input_text(default_value="++....", tag="Tukey Input")
        dpg.add_button(label="Render", callback=update_diagram, user_data=(dw, inp))
        dpg.add_text(tag="Tukey Tree")


    dpg.setup_dearpygui()
    dpg.show_item_registry()
    dpg.show_viewport()
    # dpg.maximize_viewport()
    dpg.start_dearpygui()

    dpg.destroy_context()

if __name__ == "__main__":
    main()
