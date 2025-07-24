from tkinter import ttk

def configurar_estilos():
    estilo = ttk.Style()
    estilo.theme_use('clam')  # Cambiado de 'default' a 'clam' para mejor compatibilidad visual

    estilo.configure('TLabel',
                     font=('Helvetica Neue', 11),
                     foreground='#333333',
                     padding=(4, 4))

    estilo.configure('TEntry',
                     font=('Helvetica Neue', 11),
                     padding=6,
                     relief='flat',
                     foreground='#222',
                     fieldbackground='#f4f4f4',
                     background='#f4f4f4',
                     borderwidth=1)

    estilo.configure('TButton',
                     font=('Helvetica Neue', 11, 'bold'),
                     foreground='white',
                     background='#4a90e2',
                     padding=(12, 6),
                     borderwidth=0)

    estilo.map('TButton',
               background=[('active', '#357ABD')])
