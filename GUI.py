import tkinter as tk

class TexasHoldem(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

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
        tk.Label(self, text="Welcome to Texas Holdem App form Team1").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Open page one",
                  command=lambda: master.switch_frame(PageOne)).pack()
        tk.Button(self, text="Open page two",
                  command=lambda: master.switch_frame(PageTwo)).pack()
        #welcomepanel = tk.PhotoImage(tk.Image.open("texas-holdem-poker.png")


class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is page one").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()


class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is page two").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()

if __name__ == "__main__":
    app = TexasHoldem()
    app.mainloop()
