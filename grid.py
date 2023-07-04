import tkinter as tk
from tkinter import Canvas, Button, Label

EXTRA_HEIGHT = 200


class GridUI:

    box_size = 50
    team_index_y = 540

    def __init__(self, game_obj, initial_grid, grid_size, teams_dict, empty_color="white"):
        self._root = tk.Tk()
        self.empty_color = empty_color
        self.grid_size = grid_size
        self.boxes = {}
        self.label_space = 50
        self.current_grid = initial_grid
        self.game = game_obj
        self.teams = teams_dict
        self.names_to_colors = {}
        for color,obj in self.teams.items():
            self.names_to_colors[obj.get_name()] = color
        self.change_none_and_strings_to_colors()
        self.setup_ui()

    def setup_ui(self):
        self.canvas = Canvas(self._root, width=self.box_size * self.grid_size + 2 * self.label_space,
                             height=self.box_size * self.grid_size + 2 * self.label_space + EXTRA_HEIGHT)
        self.canvas.pack()
        # Create the boxes with an offset
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.boxes[(j, i)] = self.canvas.create_rectangle(j*self.box_size + self.label_space, i*self.box_size + self.label_space,
                                                                  (j+1)*self.box_size + self.label_space,
                                                                  (i+1)*self.box_size + self.label_space,
                                                                  fill=self.empty_color)
        label_space = 50  # adjust this as needed
        label_font = ("Helvetica", 9)  # choose your font and size
        label_color = "#757575"  # choose your color

        # Add column labels
        for j in range(self.grid_size):
            self.canvas.create_text((j+0.5)*self.box_size + label_space, label_space/2 + 10,
                                    text=f"Col {j+1}", font=label_font, fill=label_color)
        # Add row labels
        for i in range(self.grid_size):
            self.canvas.create_text(label_space/2, (i+0.5)*self.box_size + label_space,
                                    text=f"Row {i+1}", font=label_font, fill=label_color)

        # Frame for the Log box
        log_frame = tk.Frame(self._root)
        log_frame.pack(side=tk.BOTTOM)

        button = Button(self._root, text="Next turn", command=self.next_turn, width=20, height=2)
        button.pack()
        button.place(x=10, y=520)  # Place the button at a specific position

        # Add a Text widget for the log box to the log_frame
        self.log = tk.Text(log_frame, state='disabled', width=70, height=20)
        self.log.pack(fill=tk.BOTH, expand=True)  # use fill and expand to make the log box resizable

        self.paint_index()


    def log_line(self, line):
        # Enable the widget, add the line, then disable it
        self.log.config(state='normal')
        self.log.insert(tk.END, str(line) + "\n")
        self.log.config(state='disabled')
        self.log.see(tk.END)  # Scroll the Text widget to show the new line

    def paint_index(self):

        label_font = ("Helvetica", 12)  # choose your font and size
        label_color = "#f0f0f0"  # choose your color
        label = Label(self._root, text="Teams:")
        label.pack()
        label.place(x=360, y=self.team_index_y-30)
        for name, color in self.names_to_colors.items():
            label = Label(self._root, text=name, bg=color, font=label_font, fg=label_color)
            label.pack()
            label.place(x=360, y=self.team_index_y)
            self.team_index_y += 30  # Increase y coordinate for next team

    def next_turn(self):
        self.game.play_one_turn()

    def change_none_and_strings_to_colors(self):
        new_grid = []
        # Change all None to White
        for i in range(self.grid_size):
            new_grid.append([])
            for j in range(self.grid_size):
                if self.current_grid[i][j] == None:
                    new_grid[i].append(self.empty_color)
                else:
                    if self.current_grid[i][j] in self.names_to_colors.keys():
                        new_grid[i].append(self.names_to_colors[self.current_grid[i][j]])
        self.current_grid = new_grid

    def animate_color_change_fade(self, box, final_color, duration=800):
        empty_color = self.canvas.itemcget(self.boxes[box], "fill")
        final_color = final_color if final_color else self.empty_color  # If color is None, revert to initial color
        initial_rgb = self._root.winfo_rgb(empty_color)
        final_rgb = self._root.winfo_rgb(final_color)

        steps = 10
        rgb_steps = [(fr - ir)/steps for ir, fr in zip(initial_rgb, final_rgb)]

        def animate(step):
            r, g, b = [int(ir + step*dr) for ir, dr in zip(initial_rgb, rgb_steps)]
            color = "#%4.4x%4.4x%4.4x" % (r, g, b)
            self.canvas.itemconfig(self.boxes[box], fill=color)
            if step < steps:
                self._root.after(duration // steps, animate, step+1)

        animate(0)


    def update_grid(self, new_grid):
        previous_grid = self.current_grid
        self.current_grid = new_grid
        self.change_none_and_strings_to_colors()

        for j in range(self.grid_size):
            for i in range(self.grid_size):
                new_color = self.current_grid[j][i] if new_grid[j][i] else self.empty_color  # If color is None, revert to initial color
                if new_color != previous_grid[j][i]:
                    self.animate_color_change_fade((i, j), new_color)
        self.current_grid = new_grid


    def update_gui(self):
        self._root.update()

    def is_valid_color(color):
        root = tk.Tk()
        root.withdraw()
        try:
            root.winfo_rgb(color)
            return True
        except tk.TclError:
            return False
        finally:
            root.destroy()

