import tkinter as tk
from tkinter.font import Font
import copy
from timer import debug_timer

"""APP"""


class App(tk.Tk):

    def __init__(self):
        super().__init__()

        self.canvas_frame = tk.Frame(self)
        self.canvas_frame.pack()

        self.canvas = tk.Canvas(self.canvas_frame)
        self.canvas.pack()

        self.rects = {}
        self.states = {}

        self.create_grid(200, 200)

    @debug_timer
    def create_grid(self, x_range, y_range, rect_size=10, rect_padding=1):

        for y in range(y_range):
            for x in range(x_range):

                x0_coords = x*rect_size + (x*rect_padding) + 2
                y0_coords = y*rect_size + (y*rect_padding) + 2
                x1_coords = x0_coords+rect_size
                y1_coords = y0_coords+rect_size

                self.rects[x, y] = self.canvas.create_rectangle(x0_coords, y0_coords, x1_coords, y1_coords,
                                                                fill="white", outline="")

                self.states[x, y] = 0

    @debug_timer
    def update_grid(self, new_grid_states):
        update_counter = 0

        for x, y in new_grid_states:
            # Only update instances that have been changed
            if new_grid_states[x, y] != self.states[x, y]:
                # Update canvas rectangle drawing
                self.canvas.itemconfig(self.rects[x, y], fill="black" if new_grid_states[x, y] == 1 else "white")

                # Update class states
                self.states[x, y] = new_grid_states[x, y]

                update_counter += 1

        print(f"Updated {update_counter} instances")

    def print_grid_states(self):
        start_y = 0
        for x, y in self.states:
            print(("\n" if y != start_y else "") + str(self.states[x, y]), end=" ")
            start_y = y
        print()


"""MAIN"""

if __name__ == "__main__":
    app = App()
    # app.eval('tk::PlaceWindow . center')  # Start app window in center of screen

    new_states = copy.deepcopy(app.states)
    new_states[3, 5] = 1
    new_states[5, 5] = 1
    new_states[1, 10] = 1

    app.update_grid(new_states)

    app.mainloop()
