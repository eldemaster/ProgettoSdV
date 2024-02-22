import tkinter as tk
from tkinter import filedialog as fd
from tkinter import Label, messagebox
import cv2
from tkinter import PhotoImage



def center_window(window):
    # Centra la finestra rispetto allo schermo
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() - width) // 2
    y = (window.winfo_screenheight() - height) // 2
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

def choose_file():
    file_path = fd.askopenfilename(title="Choose a File", filetypes=[("Image files", "*.jpg *.png")] )
    
    if file_path and not file_path.lower().endswith(('.png', '.jpg')):
        messagebox.showwarning("Formato non supportato", "Seleziona un file con formato .png o .jpg")
        return None
    file_path = str(file_path)
    return file_path

def create_new_window():
    global image_path

    # Chiudi la finestra principale
    root.withdraw()

    # Funzione per creare una nuova finestra
    new_window = tk.Toplevel()
    new_label = tk.Label(new_window, text="Nuova Finestra!")
    new_label.pack()

    # Visualizza l'immagine nella nuova finestra
    if image_path:
        image_label = tk.Label(new_window, text="Immagine Selezionata:")
        image_label.pack()

        try:
            # Apri l'immagine con OpenCV
            img_cv2 = cv2.imread(image_path)

            # Converte da BGR (formato OpenCV) a RGB (formato Tkinter)
            img_rgb = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2RGB)

            # Ridimensiona l'immagine alla metà delle sue dimensioni originali
            img_rgb = cv2.resize(img_rgb, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)

            # Converte l'immagine in un formato Tkinter compatibile
            img_tk = PhotoImage(data=cv2.imencode('.ppm', img_rgb)[1].tobytes())

            image_display = tk.Label(new_window, image=img_tk)
            image_display.image = img_tk
            image_display.pack()
        except Exception as e:
            messagebox.showerror("Errore", f"Impossibile visualizzare l'immagine selezionata: {str(e)}")

    # Bottone per tornare alla finestra principale
    back_button = tk.Button(new_window, text="Torna alla Finestra Principale", command=lambda: [new_window.destroy(), root.deiconify()])
    back_button.pack()

    # Centra la nuova finestra
    center_window(new_window)
    
        
def main():
    global root, image_path
    root = tk.Tk()
    root.title("Finestra Principale")

    # Variabile globale per salvare il percorso dell'immagine
    image_path = ""

    # Campo per l'immagine
    image_label = tk.Label(root, text="Immagine:")
    image_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)

    # Pulsante per aprire il file manager e selezionare un'immagine
    browse_button = tk.Button(root, text="Sfoglia", command=lambda: [choose_file_and_update_label()])
    browse_button.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

    # Creazione di campi di testo e relative etichette
    for i in range(1, 9):
        label = tk.Label(root, text=f"Campo {i}:")
        label.grid(row=i, column=0, padx=10, pady=10, sticky=tk.E)

        entry = tk.Entry(root)
        entry.grid(row=i, column=1, padx=10, pady=10, sticky=tk.W)

    # Creazione di un pulsante per creare una nuova finestra
    button = tk.Button(root, text="Apri Nuova Finestra", command=create_new_window)
    button.grid(row=9, columnspan=2, pady=10)

    # Centra la finestra principale
    center_window(root)

    # Avvio del loop principale dell'applicazione
    root.mainloop()

def choose_file_and_update_label():
    global image_path
    image_path = choose_file()


if __name__ == "__main__":
    main()