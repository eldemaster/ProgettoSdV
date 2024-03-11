import tkinter as tk
from calibrazioneCamera import CalibrazioneCamera
from structure import FlowMenu

def main():
    root = tk.Tk()

    # Creazione della finestra principale di FlowMenu
    flow_menu_app = FlowMenu(root, open_calibrazione_camera())

    root.mainloop()

def open_calibrazione_camera(root):
    # Chiudi la finestra principale di FlowMenu
    root.withdraw()

    # Creazione della finestra di CalibrazioneCamera
    calibrazione_camera_app = CalibrazioneCamera(tk.Toplevel(root))

if __name__ == "__main__":
    main()
