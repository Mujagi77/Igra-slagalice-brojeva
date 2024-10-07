import sys
import os
import tkinter as tk
from tkinter import messagebox
import random
import pygame
import time

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Slagalica:
    def __init__(self, root):
        self.root = root
        self.root.title("Slagalica")

        # Define themes
        self.themes = {
            "dark": {
                "bg_color": "black",
                "button_bg": "#404040",
                "button_fg": "lightgreen",
                "tile_bg": "#404040",
                "tile_fg": "lightgreen",
                "empty_bg": "#D3D3D3",
                "empty_fg": "black",
                "text_color": "white",
                "button_border": "#333333"
            },
            "light": {
                "bg_color": "white",
                "button_bg": "#D3D3D3",
                "button_fg": "black",
                "tile_bg": "#D3D3D3",
                "tile_fg": "black",
                "empty_bg": "#F0F0F0",
                "empty_fg": "black",
                "text_color": "black",
                "button_border": "#CCCCCC"
            },
            "blue": {
                "bg_color": "#001f3f",
                "button_bg": "#0074D9",
                "button_fg": "white",
                "tile_bg": "#0074D9",
                "tile_fg": "white",
                "empty_bg": "#7FDBFF",
                "empty_fg": "black",
                "text_color": "white",
                "button_border": "#0056A0"
            }
        }

        # Set initial theme
        self.current_theme = "dark"

        # Initialize pygame for sound
        pygame.mixer.init()
        self.move_sound = pygame.mixer.Sound(resource_path("move.wav"))
        self.win_sound = pygame.mixer.Sound(resource_path("win.wav"))

        # Create frame before calling apply_theme
        self.frame = tk.Frame(self.root)
        self.frame.grid(row=0, column=0, padx=20, pady=20)

        self.tiles = []
        self.empty_tile = (4, 4)

        # Add move counter
        self.move_counter = tk.Label(self.root, text="Moves: 0", font=('Helvetica', 12))
        self.move_counter.grid(row=2, column=0, pady=10)
        self.moves = 0

        # Add timer
        self.timer_label = tk.Label(self.root, text="Time: 0:00", font=('Helvetica', 12))
        self.timer_label.grid(row=1, column=0, pady=10)
        self.start_time = time.time()
        self.update_timer()

        # Set up buttons in a row
        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.grid(row=3, column=0, pady=10)

        # Interaction buttons
        self.restart_button = tk.Button(self.buttons_frame, text="Kreni iz početka", command=self.restart_game, font=('Helvetica', 12))
        self.restart_button.grid(row=0, column=0, padx=10)

        self.exit_button = tk.Button(self.buttons_frame, text="Izađi iz igre", command=self.exit_game, font=('Helvetica', 12))
        self.exit_button.grid(row=0, column=1, padx=10)

        self.tutorial_button = tk.Button(self.buttons_frame, text="Tutorijal", command=self.show_tutorial, font=('Helvetica', 12))
        self.tutorial_button.grid(row=0, column=2, padx=10)

        self.rules_button = tk.Button(self.buttons_frame, text="Pravila", command=self.show_rules, font=('Helvetica', 12))
        self.rules_button.grid(row=0, column=3, padx=10)

        self.about_button = tk.Button(self.buttons_frame, text="O autoru", command=self.show_about, font=('Helvetica', 12))
        self.about_button.grid(row=0, column=4, padx=10)

        # Theme change buttons
        self.theme_button_dark = tk.Button(self.buttons_frame, text="Tamna Tema", command=lambda: self.change_theme("dark"), font=('Helvetica', 12))
        self.theme_button_dark.grid(row=1, column=0, padx=10)

        self.theme_button_light = tk.Button(self.buttons_frame, text="Svetla Tema", command=lambda: self.change_theme("light"), font=('Helvetica', 12))
        self.theme_button_light.grid(row=1, column=1, padx=10)

        self.theme_button_blue = tk.Button(self.buttons_frame, text="Plava Tema", command=lambda: self.change_theme("blue"), font=('Helvetica', 12))
        self.theme_button_blue.grid(row=1, column=2, padx=10)

        # Apply theme and create grid
        self.apply_theme()
        self.create_grid()

        def is_solvable(self, board):
        """Proverava da li je slagalica rešiva."""
        one_d_board = [num for row in board for num in row if num != ""]

        # Brojanje inverzija
        inversions = 0
        for i in range(len(one_d_board)):
            for j in range(i + 1, len(one_d_board)):
                if one_d_board[i] > one_d_board[j]:
                    inversions += 1

        empty_row = self.empty_tile[0] + 1  # Red praznog polja (počinjemo od 1)

        # Pravilo za rešivost 5x5 slagalice
        return (empty_row % 2 == 0 and inversions % 2 != 0) or (empty_row % 2 != 0 and inversions % 2 == 0)

    def create_grid(self):
        while True:  # Loop until we find a solvable configuration
            numbers = list(range(1, 25))
            random.shuffle(numbers)
            numbers.append("")  # Empty tile

            # Check if the generated board is solvable
            if self.is_solvable([numbers[i:i + 5] for i in range(0, 25, 5)]):
                break  # Exit loop if solvable

        for i in range(5):
            row = []
            for j in range(5):
                num = numbers.pop(0)
                if num == "":
                    btn = tk.Button(self.frame, text=num, bg=self.themes[self.current_theme]["empty_bg"],
                                    fg=self.themes[self.current_theme]["empty_fg"], font=('Helvetica', 24, 'bold'),
                                    width=6, height=3)
                    self.empty_tile = (i, j)
                else:
                    btn = tk.Button(self.frame, text=str(num), bg=self.themes[self.current_theme]["tile_bg"],
                                    fg=self.themes[self.current_theme]["tile_fg"],
                                    font=('Helvetica', 24, 'bold'), width=6, height=3)
                btn.grid(row=i, column=j, padx=4, pady=4)
                btn.config(command=lambda btn=btn, i=i, j=j: self.move_tile(btn, i, j))
                row.append(btn)
            self.tiles.append(row)

    def move_tile(self, btn, i, j):
        ei, ej = self.empty_tile
        if abs(ei - i) + abs(ej - j) == 1:  # Check if move is valid
            self.tiles[ei][ej].config(text=btn["text"], bg=self.themes[self.current_theme]["tile_bg"], fg=self.themes[self.current_theme]["tile_fg"])
            btn.config(text="", bg=self.themes[self.current_theme]["empty_bg"])
            self.empty_tile = (i, j)
            self.move_sound.play()  # Play move sound
            self.moves += 1
            self.move_counter.config(text=f"Moves: {self.moves}")
            self.check_win()

    def update_timer(self):
        elapsed_time = time.time() - self.start_time
        minutes, seconds = divmod(int(elapsed_time), 60)
        self.timer_label.config(text=f"Time: {minutes}:{seconds:02d}")
        self.root.after(1000, self.update_timer)

    def check_win(self):
        correct = 1
        for i in range(5):
            for j in range(5):
                num = self.tiles[i][j]["text"]
                if num and int(num) != correct:
                    return
                correct += 1
        self.win_animation()

    def win_animation(self):
        self.win_sound.play()  # Play win sound
        for _ in range(3):
            self.frame.config(bg="green")
            self.root.update_idletasks()
            self.root.after(300)
            self.frame.config(bg=self.themes[self.current_theme]["bg_color"])
            self.root.update_idletasks()
            self.root.after(300)
        messagebox.showinfo("Čestitamo!",
                            f"Hvala na igri! Čestitamo na uspešnom rešavanju slagalice. Ukupno poteza: {self.moves}")

    def restart_game(self):
        self.frame.destroy()
        self.frame = tk.Frame(self.root)
        self.frame.grid(row=0, column=0, padx=20, pady=20)
        self.tiles = []
        self.empty_tile = (4, 4)
        self.moves = 0
        self.move_counter.config(text="Moves: 0")
        self.create_grid()
        self.start_time = time.time()  # Restart timer

    def exit_game(self):
        self.root.destroy()

    def show_tutorial(self):
        messagebox.showinfo("Tutorijal",
                            "Cilj igre je da poređate brojeve od 1 do 24, tako što pomerate polja jedno po jedno.")

    def show_rules(self):
        messagebox.showinfo("Pravila",
                            "1. Pomerajte brojeve jedan po jedan tako da prazan prostor bude pored broja koji želite da pomerite.\n"
                            "2. Kretanje brojeva se vrši pomoću dugmadi.\n"
                            "3. Pobedićete kada svi brojevi budu u ispravnom redosledu.")

    def show_about(self):
        messagebox.showinfo("O autoru",
                            "Autor: Miljan Rancic (Mujagi77)\nEmail: mujagi77@gmail.com")

    def change_theme(self, theme_name):
        self.current_theme = theme_name
        self.apply_theme()

    def apply_theme(self):
        theme = self.themes[self.current_theme]
        self.root.config(bg=theme["bg_color"])
        self.frame.config(bg=theme["bg_color"])
        for row in self.tiles:
            for btn in row:
                if btn["text"] == "":
                    btn.config(bg=theme["empty_bg"], fg=theme["empty_fg"])
                else:
                    btn.config(bg=theme["tile_bg"], fg=theme["tile_fg"])
        self.move_counter.config(bg=theme["bg_color"], fg=theme["text_color"])
        self.timer_label.config(bg=theme["bg_color"], fg=theme["text_color"])
        for widget in self.buttons_frame.winfo_children():
            widget.config(bg=theme["button_bg"], fg=theme["button_fg"], borderwidth=1, relief="solid")

if __name__ == "__main__":
    root = tk.Tk()
    app = Slagalica(root)
    root.mainloop()
