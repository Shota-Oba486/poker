import tkinter as tk
from gui.game import PokerGameUI
from gui.home import Home

class AppController:
    def __init__(self, root):
        self.root = root
        self.current_app = None
        self.show_home_screen()

    def show_poker_game(self):
        # 現在のアプリケーションを破棄してPokerGameUIを表示
        if self.current_app is not None:
            self.current_app.destroy()
        self.current_app = PokerGameUI(self.root, self.show_home_screen,self.show_poker_game)

    def show_home_screen(self):
        # 現在のアプリケーションを破棄してAnotherGameUIを表示
        if self.current_app is not None:
            self.current_app.destroy()
        self.current_app = Home(self.root, self.show_poker_game)

if __name__ == "__main__":
    root = tk.Tk()
    app_controller = AppController(root)
    root.mainloop()
