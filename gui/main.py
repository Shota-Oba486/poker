import tkinter as tk
from gui.appcontroller import AppController

if __name__ == "__main__":
    root = tk.Tk()
    app_controller = AppController(root)
    root.mainloop()