import tkinter as tk
from tkinter import filedialog as fd, messagebox
import cv2
from tkinter import PhotoImage
import random

class Parameters:
    def __init__(self):
        self.param1 = tk.DoubleVar()
        self.param2 = tk.DoubleVar()
        self.param3 = tk.DoubleVar()
        self.param4 = tk.DoubleVar()
        self.param5 = tk.DoubleVar()
        self.param6 = tk.DoubleVar()
        self.param7 = tk.DoubleVar()
        self.param8 = tk.DoubleVar()
    
    def update_parameters(self, param1, param2, param3, param4, param5, param6, param7, param8):
        self.param1.set(param1)
        self.param2.set(param2)
        self.param3.set(param3)
        self.param4.set(param4)
        self.param5.set(param5)
        self.param6.set(param6)
        self.param7.set(param7)
        self.param8.set(param8)
    
    def set_default_parameters(self):
        self.param1.set(random.uniform(1, 10))
        self.param2.set(random.uniform(1, 10))
        self.param3.set(random.uniform(1, 10))
        self.param4.set(random.uniform(1, 10))
        self.param5.set(random.uniform(1, 10))
        self.param6.set(random.uniform(1, 10))
        self.param7.set(random.uniform(1, 10))
        self.param8.set(random.uniform(1, 10))


class CalibraCamera:
    def __init__(self, master):
        self.master = master
        self.master.title("Calibra Camera")

        # Contenuto del Flow 1
        self.label = tk.Label(self.master, text="Benvenuto nel Calibra Camera!")
        self.label.pack(pady=20)
        
        # Initialize the Parameters instance
        self.parameters = Parameters()
        self.parameters.set_default_parameters()
        
    def save_parameters(self):
        try:
            # Retrieve values from entry widgets
            param1 = float(self.entry_param1.get())
            param2 = float(self.entry_param2.get())
            param3 = float(self.entry_param3.get())
            param4 = float(self.entry_param4.get())
            param5 = float(self.entry_param5.get())
            param6 = float(self.entry_param6.get())
            param7 = float(self.entry_param7.get())
            param8 = float(self.entry_param8.get())

            # Update Parameters class
            self.parameters.update_parameters(param1, param2, param3, param4, param5, param6, param7, param8)

            messagebox.showinfo("Parametri Salvati", "I parametri sono stati salvati con successo.")
        except ValueError:
            messagebox.showerror("Errore", "Inserisci valori numerici validi per i parametri.")


    def choose_file(self):
        file_path = fd.askopenfilename(title="Choose a File", filetypes=[("Image files", "*.jpg *.png")] )

        if file_path and not file_path.lower().endswith(('.png', '.jpg')):
            messagebox.showwarning("Formato non supportato", "Seleziona un file con formato .png o .jpg")
            return None
        file_path = str(file_path)
        return file_path
    
    def choose_file_and_update_label(self):
        global image_path
        image_path = self.choose_file()    

    def center_window(self, window):
        # Centra la finestra rispetto allo schermo
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() - width) // 2
        y = (window.winfo_screenheight() - height) // 2
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def create_new_window(self):
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

                # Stampare le dimensioni dell'immagine originale
                print("Dimensioni originali:", img_cv2.shape)

                # Converte da BGR (formato OpenCV) a RGB (formato Tkinter)
                img_rgb = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2RGB)

                # Calcola le nuove dimensioni dell'immagine (1/4 dello schermo)
                screen_width = new_window.winfo_screenwidth()
                screen_height = new_window.winfo_screenheight()
                target_width = int(screen_width / 2)  # 1/4 dello schermo
                target_height = int(screen_height / 2)

                # Ridimensiona l'immagine in base alle nuove dimensioni
                img_rgb_resized = cv2.resize(img_rgb, (target_width, target_height), interpolation=cv2.INTER_LINEAR)

                # Stampare le nuove dimensioni dell'immagine ridotta
                print("Dimensioni ridotte:", img_rgb_resized.shape)

                # Converte l'immagine ridimensionata in un formato Tkinter compatibile
                img_tk_resized = PhotoImage(data=cv2.imencode('.ppm', img_rgb_resized)[1].tobytes())

                # Mostra l'immagine ridimensionata senza canvas
                image_display = tk.Label(new_window, image=img_tk_resized)
                image_display.image = img_tk_resized
                image_display.pack()

                # Aggiungi etichette per visualizzare i parametri
                params_label = tk.Label(new_window, text="Parametri:")
                params_label.pack()

                # Mostra i parametri a destra dell'immagine
                params_frame = tk.Frame(new_window)
                params_frame.pack(side=tk.RIGHT, padx=10)

                for i in range(1, 9):
                    param_label = tk.Label(params_frame, text=f"Param{i}: {self.parameters.__dict__[f'param{i}'].get()}")
                    param_label.pack()

            except Exception as e:
                # Stampa l'intera traccia dell'errore
                import traceback
                traceback.print_exc()
                messagebox.showerror("Errore", f"Non si vede l'immagine: {str(e)}")



        # Bottone per tornare alla finestra principale
        back_button = tk.Button(new_window, text="Torna alla Finestra Principale", command=lambda: [new_window.destroy(), root.deiconify()])
        back_button.pack()

        # Centra la nuova finestra
        self.center_window(new_window)

    def CalibraCameraMain(self):
        global root, image_path
        root = tk.Tk()
        root.title("Finestra Principale")

        # Variabile globale per salvare il percorso dell'immagine
        image_path = ""

        # Campo per l'immagine
        image_label = tk.Label(root, text="Immagine:")
        image_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)

        # Pulsante per aprire il file manager e selezionare un'immagine
        browse_button = tk.Button(root, text="Sfoglia", command=lambda: [self.choose_file_and_update_label()])
        browse_button.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        # Creazione di campi di testo e relative etichette
        for i in range(1, 9):
            label = tk.Label(root, text=f"Campo {i}:")
            label.grid(row=i, column=0, padx=10, pady=10, sticky=tk.E)

            entry = tk.Entry(root)
            entry.grid(row=i, column=1, padx=10, pady=10, sticky=tk.W)

        # Creazione di un pulsante per creare una nuova finestra
        button = tk.Button(root, text="Apri Nuova Finestra", command=self.create_new_window)
        button.grid(row=9, columnspan=2, pady=10)

        # Centra la finestra principale
        self.center_window(root)

        # Avvio del loop principale dell'applicazione
        root.mainloop()


class CalibraLaser:
    def __init__(self, master):
        self.master = master
        self.master.title("Calibra Laser")

        # Contenuto del Flow 1
        self.label = tk.Label(self.master, text="Benvenuto nel Calibra Laser!")
        self.label.pack(pady=20)
        
        # Initialize the Parameters instance
        self.parameters = Parameters()
        
        self.parameters.set_default_parameters()
        
    def save_parameters(self):
        try:
            # Retrieve values from entry widgets
            param1 = float(self.entry_param1.get())
            param2 = float(self.entry_param2.get())
            param3 = float(self.entry_param3.get())
            param4 = float(self.entry_param4.get())
            param5 = float(self.entry_param5.get())
            param6 = float(self.entry_param6.get())
            param7 = float(self.entry_param7.get())
            param8 = float(self.entry_param8.get())

            # Update Parameters class
            self.parameters.update_parameters(param1, param2, param3, param4, param5, param6, param7, param8)

            messagebox.showinfo("Parametri Salvati", "I parametri sono stati salvati con successo.")
        except ValueError:
            messagebox.showerror("Errore", "Inserisci valori numerici validi per i parametri.")


    def choose_file(self):
        file_path = fd.askopenfilename(title="Choose a File", filetypes=[("Image files", "*.jpg *.png")] )

        if file_path and not file_path.lower().endswith(('.png', '.jpg')):
            messagebox.showwarning("Formato non supportato", "Seleziona un file con formato .png o .jpg")
            return None
        file_path = str(file_path)
        return file_path
    
    def choose_file_and_update_label(self):
        global image_path
        image_path = self.choose_file()    

    def center_window(self, window):
        # Centra la finestra rispetto allo schermo
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() - width) // 2
        y = (window.winfo_screenheight() - height) // 2
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def create_new_window(self):
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
            
                # Stampare le dimensioni dell'immagine originale
                print("Dimensioni originali:", img_cv2.shape)
            
                # Converte da BGR (formato OpenCV) a RGB (formato Tkinter)
                img_rgb = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2RGB)
            
                # Calcola le nuove dimensioni dell'immagine (1/4 dello schermo)
                screen_width = new_window.winfo_screenwidth()
                screen_height = new_window.winfo_screenheight()
                target_width = int(screen_width / 2)  # 1/4 dello schermo
                target_height = int(screen_height / 2)
            
                # Ridimensiona l'immagine in base alle nuove dimensioni
                img_rgb_resized = cv2.resize(img_rgb, (target_width, target_height), interpolation=cv2.INTER_LINEAR)
            
                # Stampare le nuove dimensioni dell'immagine ridotta
                print("Dimensioni ridotte:", img_rgb_resized.shape)
            
                # Converte l'immagine ridimensionata in un formato Tkinter compatibile
                img_tk_resized = PhotoImage(data=cv2.imencode('.ppm', img_rgb_resized)[1].tobytes())
            
                # Mostra l'immagine ridimensionata senza canvas
                image_display = tk.Label(new_window, image=img_tk_resized)
                image_display.image = img_tk_resized
                image_display.pack()
            
                # Aggiungi etichette per visualizzare i parametri
                params_label = tk.Label(new_window, text="Parametri:")
                params_label.pack()
            
                # Mostra i parametri a destra dell'immagine
                params_frame = tk.Frame(new_window)
                params_frame.pack(side=tk.RIGHT, padx=10)
            
                for i in range(1, 9):
                    param_label = tk.Label(params_frame, text=f"Param{i}: {self.parameters.__dict__[f'param{i}'].get()}")
                    param_label.pack()
            
            except Exception as e:
                # Stampa l'intera traccia dell'errore
                import traceback
                traceback.print_exc()
                messagebox.showerror("Errore", f"Non si vede l'immagine: {str(e)}")




        # Bottone per tornare alla finestra principale
        back_button = tk.Button(new_window, text="Torna alla Finestra Principale", command=lambda: [new_window.destroy(), root.deiconify()])
        back_button.pack()

        # Centra la nuova finestra
        self.center_window(new_window)

    def CalibraLaserMain(self):
        global root, image_path
        root = tk.Tk()
        root.title("Finestra Principale")

        # Variabile globale per salvare il percorso dell'immagine
        image_path = ""

        # Campo per l'immagine
        image_label = tk.Label(root, text="Immagine:")
        image_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)

        # Pulsante per aprire il file manager e selezionare un'immagine
        browse_button = tk.Button(root, text="Sfoglia", command=lambda: [self.choose_file_and_update_label()])
        browse_button.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        # Creazione di campi di testo e relative etichette
        for i in range(1, 9):
            label = tk.Label(root, text=f"Campo {i}:")
            label.grid(row=i, column=0, padx=10, pady=10, sticky=tk.E)

            entry = tk.Entry(root)
            entry.grid(row=i, column=1, padx=10, pady=10, sticky=tk.W)

        # Creazione di un pulsante per creare una nuova finestra
        button = tk.Button(root, text="Apri Nuova Finestra", command=self.create_new_window)
        button.grid(row=9, columnspan=2, pady=10)

        # Centra la finestra principale
        self.center_window(root)

        # Avvio del loop principale dell'applicazione
        root.mainloop()



class MyInterface:
    def __init__(self, master):
        self.master = master
        self.master.title("Programma Principale")

        # Create Parameters instance
        self.parameters = Parameters()

        # Creazione del menu
        self.menu_frame = tk.Frame(self.master)
        self.menu_frame.pack(pady=20)

        # Pulsanti nel menu
        self.button1 = tk.Button(self.menu_frame, text="Calibrazione Camera", command=self.openCalibrazioneCamera)
        self.button1.pack(side=tk.LEFT, padx=10)

        self.button2 = tk.Button(self.menu_frame, text="Calibrazione Lama", command=self.openCalibrazioneLama)
        self.button2.pack(side=tk.LEFT, padx=10)

        self.button3 = tk.Button(self.menu_frame, text="Flow 3", command=self.openMisura)
        self.button3.pack(side=tk.LEFT, padx=10)

    
    def openCalibrazioneCamera(self):
        flow1_app = CalibraCamera(self.master)
        flow1_app.CalibraCameraMain()

    def openCalibrazioneLama(self):
        flow1_app = CalibraLaser(self.master)
        flow1_app.CalibraLaserMain()

    def openMisura(self):
        messagebox.showinfo("Flow 3", "Apri la finestra del Flow 3")
        # Aggiungi qui la logica per aprire la finestra del Flow 3

    def save_parameters(self, flow1_app):
        # Check which flow is currently active (camera or laser) and call the respective save method
        if isinstance(flow1_app, CalibraCamera):
            flow1_app.save_parameters()
        elif isinstance(flow1_app, CalibraLaser):
            flow1_app.save_parameters()


def main():
    root = tk.Tk()
    app = MyInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()
