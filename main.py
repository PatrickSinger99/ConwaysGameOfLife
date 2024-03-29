import tkinter as tk
from tkinter.font import Font
import copy
from timer import debug_timer
import random
from game_logic import *
import time


"""APP"""


class App(tk.Tk):

    @debug_timer
    def __init__(self):
        super().__init__()

        self.iconbitmap("icons/logo_large.ico")
        self.title("Conway's Game of Life")
        self.resizable(False, False)

        """COLORS"""

        # GUI
        self.accent_color = "#3366cc"

        # Grid
        self.live_cell_color = "black"
        self.dead_cell_color = "white"
        self.marked_cell_color = "orange"
        self.grid_background_color = "light grey"

        """IMAGES"""

        self.logo_bg_image = tk.PhotoImage(file="icons/logo_bg.png")

        self.reset_bg = tk.PhotoImage(file="icons/reset_bg.png")
        self.reset_fg = tk.PhotoImage(file="icons/reset_fg.png")
        self.reset_active = tk.PhotoImage(file="icons/reset_active.png")

        self.pause_bg = tk.PhotoImage(file="icons/pause_bg.png")
        self.pause_fg = tk.PhotoImage(file="icons/pause_fg.png")
        self.pause_active = tk.PhotoImage(file="icons/pause_active.png")

        self.play_bg = tk.PhotoImage(file="icons/play_bg.png")
        self.play_fg = tk.PhotoImage(file="icons/play_fg.png")
        self.play_active = tk.PhotoImage(file="icons/play_active.png")

        self.nextgen_bg = tk.PhotoImage(file="icons/nextgen_bg.png")
        self.nextgen_fg = tk.PhotoImage(file="icons/nextgen_fg.png")
        self.nextgen_active = tk.PhotoImage(file="icons/nextgen_active.png")

        """STATE VARIABLES"""

        # Grid elements
        self.cell_ids = {}
        self.cell_states = {}

        # Canvas panning
        self.pan_offset_x = 0
        self.pan_offset_y = 0
        self.pan_active = False
        self.start_x = None
        self.start_y = None
        self.zoom_level = 1

        # Gameplay
        self.current_gen = tk.IntVar()
        self.current_gen.set(0)
        self.autoplay_active = False

        self.last_update_time = time.time()
        self.actual_game_speed = 0

        self.speed_display = tk.StringVar()
        self.speed_display.set("")

        self.speed_values = [1, 0.2, 0.1, 0.05, 0.02]
        self.target_speed_value = tk.DoubleVar()
        self.target_speed_value.set(self.speed_values[2])

        # True if a stamp is selected
        self.stamp_active = False

        # TEST
        self.glider = [[0, 0, 1], [1, 0, 1], [0, 1, 1]]

        """HEADER"""

        # FRAME: Header
        self.header_frame = tk.Frame(self, bg=self.accent_color)
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        # TITLE
        self.game_title_label = tk.Label(self.header_frame, text=" Conway's Game of Life Simulation", fg="white",
                                         bg=self.header_frame["bg"], font=Font(size=14, weight="bold"),
                                         compound="left", image=self.logo_bg_image)
        self.game_title_label.pack(side="left", padx=3, pady=3)

        """CONTROL PANEL"""

        # FRAME: Control Panel
        self.control_frame = tk.Frame(self, width=300, bg="grey")
        self.control_frame.grid(row=1, column=0, sticky="ns")


        self.random_button = tk.Button(self.control_frame, text="Random", command=self.random_grid)
        self.random_button.pack()



        self.reset_zoom_button = tk.Button(self.control_frame, text="Reset View", command=self.reset_canvas_view)
        self.reset_zoom_button.pack()


        self.gen_buttons_frame = tk.Frame(self.control_frame)
        self.gen_buttons_frame.pack(padx=10)

        self.reset_button = tk.Button(self.gen_buttons_frame, text="Reset\n", command=self.reset_grid,
                                      image=self.reset_bg, compound="top", relief="flat", cursor="hand2", bd=0,
                                      bg=self.control_frame.cget("bg"), activebackground=self.control_frame.cget("bg"))
        self.reset_button.bind("<Enter>", lambda e: self.reset_button.configure(image=self.reset_fg))
        self.reset_button.bind("<Leave>", lambda e: self.reset_button.configure(image=self.reset_bg))
        self.reset_button.bind("<Button-1>", lambda e: self.reset_button.configure(image=self.reset_active))
        self.reset_button.bind("<ButtonRelease-1>", lambda e: self.reset_button.configure(image=self.reset_fg))
        self.reset_button.pack(side="left")

        self.next_get_button = tk.Button(self.gen_buttons_frame, text="Next\nGen", command=self.next_generation,
                                         image=self.nextgen_bg, compound="top", relief="flat", cursor="hand2", bd=0,
                                         bg=self.control_frame.cget("bg"), activebackground=self.control_frame.cget("bg"))
        self.next_get_button.bind("<Enter>", lambda e: self.next_get_button.configure(image=self.nextgen_fg))
        self.next_get_button.bind("<Leave>", lambda e: self.next_get_button.configure(image=self.nextgen_bg))
        self.next_get_button.bind("<Button-1>", lambda e: self.next_get_button.configure(image=self.nextgen_active))
        self.next_get_button.bind("<ButtonRelease-1>", lambda e: self.next_get_button.configure(image=self.nextgen_fg))
        self.next_get_button.pack(side="left")

        self.autoplay_button = tk.Button(self.gen_buttons_frame, text="Auto\nplay", command=self.toggle_autoplay,
                                         image=self.play_bg, compound="top", relief="flat", cursor="hand2", bd=0,
                                         bg=self.control_frame.cget("bg"), activebackground=self.control_frame.cget("bg"))
        self.autoplay_button.bind("<Enter>", lambda e: self.autoplay_button.configure(image=self.play_fg))
        self.autoplay_button.bind("<Leave>", lambda e: self.autoplay_button.configure(image=self.play_bg))
        self.autoplay_button.bind("<Button-1>", lambda e: self.autoplay_button.configure(image=self.play_active))
        self.autoplay_button.bind("<ButtonRelease-1>", lambda e: self.autoplay_button.configure(image=self.play_bg))
        self.autoplay_button.pack(side="left")

        # Speed and Generation
        self.generation_label = tk.Label(self.control_frame, textvariable=self.current_gen)
        self.generation_label.pack(side="bottom")

        self.gen_speed_label = tk.Label(self.control_frame, textvariable=self.speed_display)
        self.gen_speed_label.pack(side="bottom")

        # FRAME: Speed Controls
        self.speed_control_frame = tk.Frame(self.control_frame)
        self.speed_control_frame.pack(side="bottom")

        self.decrease_speed_button = tk.Button(self.speed_control_frame, text="-", width=2)
        self.decrease_speed_button.grid(row=0, column=0, rowspan=2, sticky="w")

        self.target_speed_label = tk.Label(self.speed_control_frame, textvariable=self.target_speed_value)
        self.target_speed_label.grid(row=1, column=1)

        self.increase_speed_button = tk.Button(self.speed_control_frame, text="+", width=2)
        self.increase_speed_button.grid(row=0, column=2, rowspan=2, sticky="e")


        """CANVAS"""

        # FRAME: Canvas
        self.canvas_frame = tk.Frame(self)
        self.canvas_frame.grid(row=1, column=1)

        # CANVAS: Displays CGOL cells
        self.canvas = tk.Canvas(self.canvas_frame, width=800, height=600, cursor="hand2", bg=self.grid_background_color,
                                highlightthickness=0, relief='ridge', bd=0)
        self.canvas.bind("<MouseWheel>", self.mouse_zoom)
        self.canvas.bind("<ButtonPress-3>", self.start_pan)
        self.canvas.bind("<ButtonRelease-3>", self.end_pan)
        self.canvas.bind("<B3-Motion>", self.update_pan)
        self.canvas.pack()

        """INITIAL CALLS"""

        self.create_grid(49, 37)

    @debug_timer
    def create_grid(self, x_range, y_range, rect_size=15, rect_padding=1):

        for y in range(y_range):
            for x in range(x_range):

                x0_coords = x*rect_size + (x*rect_padding) + 2
                y0_coords = y*rect_size + (y*rect_padding) + 2
                x1_coords = x0_coords+rect_size-1
                y1_coords = y0_coords+rect_size-1

                self.cell_ids[x, y] = self.canvas.create_rectangle(x0_coords, y0_coords, x1_coords, y1_coords,
                                                                   fill=self.dead_cell_color, outline=self.dead_cell_color,
                                                                   activeoutline=self.marked_cell_color)
                self.canvas.tag_bind(self.cell_ids[x, y], "<ButtonPress-1>", self.on_element_click)

                self.cell_states[x, y] = 0

    @debug_timer
    def update_grid(self, new_grid_states):
        update_counter = 0

        for x, y in new_grid_states:
            # Only update instances that have been changed
            if new_grid_states[x, y] != self.cell_states[x, y]:
                # Update canvas rectangle drawing
                self.canvas.itemconfig(self.cell_ids[x, y], fill=self.live_cell_color if new_grid_states[x, y] == 1 else self.dead_cell_color,
                                       outline=self.live_cell_color if new_grid_states[x, y] == 1 else self.dead_cell_color)

                # Update class states
                self.cell_states[x, y] = new_grid_states[x, y]

                update_counter += 1
        self.update()
        # print(f"Updated {update_counter} instances")

    def reset_grid(self):
        new_states = copy.deepcopy(self.cell_states)
        for cell in new_states:
            new_states[cell] = 0

        self.update_grid(new_states)

        # Reset generation
        self.current_gen.set(0)

    def random_grid(self):
        new_states = copy.deepcopy(self.cell_states)
        for cell in new_states:
            new_states[cell] = random.choice((0, 1))

        self.update_grid(new_states)

        # Reset generation
        self.current_gen.set(0)

    @debug_timer
    def next_generation(self):
        new_gen_dict = get_next_gen(self.cell_states)
        self.update_grid(new_gen_dict)
        self.current_gen.set(self.current_gen.get() + 1)

    def auto_next_gen(self):
        if self.autoplay_active:
            self.last_update_time = time.time()

            self.next_generation()

            self.actual_game_speed = time.time() - self.last_update_time
            wait_time = self.target_speed_value.get() - self.actual_game_speed
            if wait_time <= 0:
                wait_time = 0.001
            self.update_speed_display()

            self.after(int(wait_time*1000), self.auto_next_gen)

    def toggle_autoplay(self):
        if not self.autoplay_active:
            self.autoplay_button["text"] = "Pause\n"
            self.autoplay_active = True
            self.auto_next_gen()

            self.autoplay_button.bind("<Enter>", lambda e: self.autoplay_button.configure(image=self.pause_fg))
            self.autoplay_button.bind("<Leave>", lambda e: self.autoplay_button.configure(image=self.pause_bg))
            self.autoplay_button.bind("<Button-1>", lambda e: self.autoplay_button.configure(image=self.pause_active))
            self.autoplay_button.bind("<ButtonRelease-1>", lambda e: self.autoplay_button.configure(image=self.pause_bg))

        else:
            self.autoplay_button["text"] = "Auto\nplay"
            self.autoplay_active = False

            self.autoplay_button.bind("<Enter>", lambda e: self.autoplay_button.configure(image=self.play_fg))
            self.autoplay_button.bind("<Leave>", lambda e: self.autoplay_button.configure(image=self.play_bg))
            self.autoplay_button.bind("<Button-1>", lambda e: self.autoplay_button.configure(image=self.play_active))
            self.autoplay_button.bind("<ButtonRelease-1>", lambda e: self.autoplay_button.configure(image=self.play_bg))

    def change_speed(self, step):
        pass

    """EVENTS"""

    def on_element_click(self, event):
        if not self.pan_active:
            element_id = event.widget.find_closest(event.x - self.pan_offset_x, event.y - self.pan_offset_y)[0]
            dict_index = list(self.cell_ids.values()).index(element_id)
            x, y = list(self.cell_ids.keys())[dict_index]

            if not self.stamp_active:
                if self.cell_states[x, y] == 0:
                    self.canvas.itemconfig(element_id, fill=self.live_cell_color, outline=self.live_cell_color)
                    self.cell_states[x, y] = 1
                else:
                    self.canvas.itemconfig(element_id, fill=self.dead_cell_color, outline=self.dead_cell_color)
                    self.cell_states[x, y] = 0
            else:
                for stamp_y in range(len(self.glider)):
                    for stamp_x in range(len(self.glider[stamp_y])):

                        if self.glider[stamp_y][stamp_x] == 1:
                            self.canvas.itemconfig(self.cell_ids[x + stamp_x, y + stamp_y], fill=self.live_cell_color, outline=self.live_cell_color)
                            self.cell_states[x + stamp_x, y + stamp_y] = 1
                        else:
                            self.canvas.itemconfig(self.cell_ids[x + stamp_x, y + stamp_y], fill=self.dead_cell_color, outline=self.dead_cell_color)
                            self.cell_states[stamp_x + x, stamp_y + y] = 0

    def mouse_zoom(self, event):

        if event.delta > 0:
            self.canvas.scale("all", self.canvas.winfo_width() / 2 - self.pan_offset_x,
                              self.canvas.winfo_height() / 2 - self.pan_offset_y, 1.2, 1.2)

            self.zoom_level *= 1.2

        elif event.delta < 0:
            self.canvas.scale("all", self.canvas.winfo_width() / 2 - self.pan_offset_x,
                              self.canvas.winfo_height() / 2 - self.pan_offset_y, 0.8, 0.8)

            self.zoom_level *= 0.8

    def reset_canvas_view(self):

        print(self.canvas.xview()[0], self.canvas.yview()[0])

        self.canvas.scale("all", self.canvas.winfo_width() / 2 - self.pan_offset_x,
                          self.canvas.winfo_height() / 2 - self.pan_offset_y, 1/self.zoom_level, 1/self.zoom_level)

        self.zoom_level = 1

    def start_pan(self, event):
        self.start_x = event.x
        self.start_y = event.y

        self.canvas.scan_mark(event.x, event.y)

    def end_pan(self, event):
        self.canvas["cursor"] = "hand2"
        self.pan_active = False

        self.canvas.scan_dragto(event.x, event.y, gain=1)

        # update pan offset
        self.pan_offset_x += event.x - self.start_x
        self.pan_offset_y += event.y - self.start_y

    def update_pan(self, event):
        if not self.pan_active:
            self.canvas["cursor"] = "fleur"
            self.pan_active = True

        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def update_speed_display(self):
        gens_per_second = round(1 / self.actual_game_speed)

        try:
            target_per_second = round(1 / self.target_speed_value.get())
        except ZeroDivisionError:
            target_per_second = 9999

        displayed_speed = min([gens_per_second, target_per_second])

        self.speed_display.set(str(displayed_speed) + " Gen/sek")

        # Color

        difference = min([gens_per_second / target_per_second, 1])

        gradient = {0.5: "#FF0D0D", 0.6: "#FF4E11", 0.7: "#FF8E15", 0.8: "#FAB733", 0.9: "#ACB334", 1: "#69B34C"}
        for key in gradient:
            if difference <= key:
                self.gen_speed_label.configure(fg=gradient[key])
                break

    """DEBUG"""

    def print_grid_states(self):
        start_y = 0
        for x, y in self.cell_states:
            print(("\n" if y != start_y else "") + str(self.cell_states[x, y]), end=" ")
            start_y = y
        print()


"""MAIN"""

if __name__ == "__main__":
    app = App()
    # app.eval('tk::PlaceWindow . center')  # Start app window in center of screen
    app.mainloop()
