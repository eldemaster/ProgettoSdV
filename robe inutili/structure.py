import tkinter as tk
from tkinter import messagebox

class FlowMenu:
    def __init__(self, master, calibrazione_callback):
        self.master = master
        self.master.title("Programma Principale")

        # Centra la finestra principale
        self.center_window()

        # Creazione del menu
        self.menu_frame = tk.Frame(self.master)
        self.menu_frame.pack(pady=20)

        # Pulsanti nel menu (verticale)
        self.button1 = tk.Button(self.menu_frame, text="Flow 1", command=calibrazione_callback)
        self.button1.pack(pady=10)

        self.button2 = tk.Button(self.menu_frame, text="Flow 2", command=self.open_flow_2)
        self.button2.pack(pady=10)

        self.button3 = tk.Button(self.menu_frame, text="Flow 3", command=self.open_flow_3)
        self.button3.pack(pady=10)

    def open_flow_1(self):
        messagebox.showinfo("Flow 1", "Apri la finestra del Flow 1")
        # Aggiungi qui la logica per aprire la finestra del Flow 1

    def open_flow_2(self):
        messagebox.showinfo("Flow 2", "Apri la finestra del Flow 2")
        # Aggiungi qui la logica per aprire la finestra del Flow 2

    def open_flow_3(self):
        messagebox.showinfo("Flow 3", "Apri la finestra del Flow 3")
        # Aggiungi qui la logica per aprire la finestra del Flow 3

    def center_window(self):
        # Centra la finestra rispetto allo schermo
        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        x = (self.master.winfo_screenwidth() - width) // 2
        y = (self.master.winfo_screenheight() - height) // 2
        self.master.geometry('{}x{}+{}+{}'.format(width, height, x, y))
