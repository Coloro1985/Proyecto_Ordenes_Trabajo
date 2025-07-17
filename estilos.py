from tkinter import ttk

def configurar_estilos():
    estilo = ttk.Style()
    estilo.configure('TButton',
                     font=('Helvetica', 12),
                     foreground='white',
                     background='#007ACC',
                     padding=10)
    estilo.configure('TLabel', font=('Arial', 10), foreground='green')
    # Añade más configuraciones de estilo según tus necesidades
