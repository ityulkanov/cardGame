import tkinter as tk
from time import sleep
from tkinter import messagebox
from client import Client

from PIL import *
from PIL import Image, ImagecTk


class TexasHoldem(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)
        self.title('TexasPoker')

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Welcome to Texas Holdem App from Team1").pack(side="top", fill="x", pady=10)
        tk.Entry(self, show="Login here").pack(side="top", fill="x", pady=11)
        tk.Button(self, text="Login",
                  command=lambda: master.switch_frame(InGamePage).bind("<Button-1>", log_in)).pack()

        tk.Button(self, text="Join Game",
                  command=lambda: master.switch_frame(InGamePage).bind("<Button-1>", join_game)).pack()

        tk.Image(self, command=open("img//texas-holdem-poker.png"))


class InGamePage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Welcome!").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()


if __name__ == "__main__":
    app = TexasHoldem()
    tableimg = Image.open("img//table.jpg")
    shirt = Image.open("img//shirts//red_back.png")

    sleep(0.01)
    app.mainloop()
