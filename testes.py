





import tkinter as tk
from tkinter import PhotoImage
class WindowTooltip():
    
    def __init__(self,parent):    
        self.parent = parent
        self.popup = tk.Toplevel(self.parent)
    def on_enter(self,event):
        # Aparecer a janela flutuante
        self.popup.geometry(f"200x100+{event.x_root+10}+{event.y_root+10}")
        self.popup.deiconify()

    def on_leave(self):
        # Esconder a janela flutuante
        self.popup.withdraw()

    # Janela principal
    # Adicionar uma imagem (substitua pelo caminho da sua imagem)
    def Create(self,ActivationLabel):

        # Criar a janela flutuante
    
        self.popup.withdraw()  # Esconda inicialmente
        self.popup.overrideredirect(True)  # Remova a barra de título
        self.popup.attributes("-topmost", True)  # Sempre acima

        # Adicionar um Frame à janela flutuante
        popup_frame = tk.Frame(self.popup, bg="lightblue", padx=10, pady=10)
        popup_frame.pack(fill="both", expand=True)

        # Adicionar conteúdo ao Frame
        label = tk.Label(popup_frame, text="Conteúdo Personalizado", bg="lightblue")
        label.pack()

        # Associar eventos de mouse à imagem
        ActivationLabel.bind("<Enter>", lambda x: self.on_enter(x))
        ActivationLabel.bind("<Leave>", lambda x: self.on_leave())
# Janela principal
root = tk.Tk()
root.title("Janela Principal")
root.geometry("400x300")

# Manter a janela principal sempre no topo
root.attributes("-topmost", True)
root.overrideredirect(True)
Lbl = tk.Label(root,text="Teste")
Lbl.pack()
WindowTooltip(root).Create(Lbl)
# Adicionar uma imagem (substitua pelo caminho da sua imagem)
image = PhotoImage(width=100, height=100)  # Imagem de exemplo
image_canvas = tk.Label(root,text="Fs")
image_canvas.pack(pady=50)


root.mainloop()