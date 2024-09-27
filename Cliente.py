
import tkinter as tk
from tkinter import messagebox, ttk




class ClienteApp(tk.Tk):
    def __init__(self, *args):
        super().__init__(*args)
        self.main_sceen()
    
    def main_sceen(self):
        self.geometry("800x600")
        self.title("Area do Cliente")

        frame_dash = tk.Frame(self, width=1920, height=100, bg="#AA6C39")
        frame_dash.pack()
        frame_dash.propagate(False)

        frame_pesquisa = tk.Frame(frame_dash)
        frame_pesquisa.pack()

if __name__ == "__main__":
    app = ClienteApp()
    app.mainloop()


        