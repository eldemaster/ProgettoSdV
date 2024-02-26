import tkinter as tk
from tkinter import filedialog as fd, messagebox
import cv2
from tkinter import PhotoImage
from structure import FlowMenu

class CalibrazioneCamera:
    def __init__(self, master):
        self.master = master
        self.master.title("Calibrazione Camera")

        # Variabili per la gestione dell'immagine
        self.image_path = ""

        # Creazione del menu dei flow utilizzando la classe FlowMenu
        self.flow_menu = FlowMenu(self.master, self.open_flow_1)

        # Campo per l'immagine
        self.image_label = tk.Label(self.master, text="Immagine:")
        self.image_label.grid(row=0, column=2, padx=10, pady=10, sticky=tk.E)

        # Pulsante per aprire il file manager e selezionare un'immagine
        self.browse_button = tk.Button(self.master, text="Sfoglia", command=self.choose_file_and_update_label)
        self.browse_button.grid(row=0, column=3, padx=10, pady=10, sticky=tk.W)

        # Creazione di campi di testo e relative etichette
        for i in range(1, 9):
            label = tk.Label(self.master, text=f"Campo {i}:")
            label.grid(row=i, column=2, padx=10, pady=10, sticky=tk.E)

            entry = tk.Entry(self.master)
            entry.grid(row=i, column=3, padx=10, pady=10, sticky=tk.W)

        # Creazione di un pulsante per creare una nuova finestra
        self.button = tk.Button(self.master, text="Apri Nuova Finestra", command=self.create_new_window)
        self.button.grid(row=9, columnspan=2, pady=10)

        # Centra la finestra principale
        self.center_window()

    def open_flow_1(self):
        messagebox.showinfo("Flow 1", "Apri la finestra del Flow 1")
        # Aggiungi qui la logica per aprire la finestra del Flow 1

    def create_new_window(self):
        # Chiudi la finestra principale
        self.master.withdraw()

        # Funzione per creare una nuova finestra
        new_window = tk.Toplevel(self.master)
        new_label = tk.Label(new_window, text="Nuova Finestra!")
        new_label.pack()

        # Resto del codice per la nuova finestra...

    def choose_file_and_update_label(self):
        self.image_path = self.choose_file()    

    def choose_file(self):
        file_path = fd.askopenfilename(title="Choose a File", filetypes=[("Image files", "*.jpg *.png")] )

        if file_path and not file_path.lower().endswith(('.png', '.jpg')):
            messagebox.showwarning("Formato non supportato", "Seleziona un file con formato .png o .jpg")
            return None
        file_path = str(file_path)
        return file_path
    
    def center_window(self):
        # Centra la finestra rispetto allo schermo
        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        x = (self.master.winfo_screenwidth() - width) // 2
        y = (self.master.winfo_screenheight() - height) // 2
        self.master.geometry('{}x{}+{}+{}'.format(width, height, x, y))

def main():
    root = tk.Tk()
    app = CalibrazioneCamera(root)
    root.mainloop()

if __name__ == "__main__":
    main()
