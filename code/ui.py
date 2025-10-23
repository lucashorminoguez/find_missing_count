import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from PIL import Image, ImageTk, ImageSequence
import sys, os

from text_message import text_data 
from logic import encontrar_faltantes

if getattr(sys, 'frozen', False):
    BASE_PATH = sys._MEIPASS 
else:
    BASE_PATH = os.path.dirname(__file__)

def resource_path(relative_path):
    """Devuelve la ruta válida tanto en ejecución normal como empaquetada con PyInstaller."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath(".."), relative_path)



gif_path = resource_path("resources/meme.gif")
icon_path = resource_path("resources/icono.ico")



class BuscadorApp:
    def __init__(self, root):
        self.root = root
        self.current_lang = 'ES'
        self.delay = 100
        
        self.configurar_ventana()
        self.crear_widgets()
        self.cargar_recursos()

    def configurar_ventana(self):
        self.root.title(text_data[self.current_lang]['title'])
        self.root.geometry("700x500")
        self.root.minsize(550, 450)
        self.root.configure(bg="#2E3440")
        try:
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"No se pudo asignar el ícono: {e}")

    def cargar_recursos(self):
        self.label_gif = tk.Label(self.root, bg="#2E3440") 
        try:
            pil_gif = Image.open(gif_path)
            frames = [ImageTk.PhotoImage(frame.copy().convert("RGBA")) for frame in ImageSequence.Iterator(pil_gif)]
            self.delay = pil_gif.info.get("duration", 100)
            self.label_gif.frames = frames
        except Exception as e:
            print(f"No se pudo cargar el GIF: {e}")
            self.label_gif.frames = []

    def crear_widgets(self):
        fuente_label = ("Segoe UI", 11)
        fuente_entry = ("Segoe UI", 11)
        fuente_btn = ("Segoe UI", 11, "bold")
        fuente_text = ("Consolas", 11)

        frame_top = tk.Frame(self.root, bg="#2E3440")
        frame_top.pack(fill="x", padx=10, pady=5)

        self.lang_menu_button = tk.Menubutton(
            frame_top, 
            text=text_data[self.current_lang]['idioma'], 
            font=("Segoe UI", 9), 
            bg="#4C566A", 
            fg="#ECEFF4",
            relief="raised",
            bd=2
        )
        lang_menu = tk.Menu(self.lang_menu_button, tearoff=0)
        self.lang_menu_button.config(menu=lang_menu)
        lang_menu.add_command(label="Español", command=lambda: self.cambiar_idioma('ES'))
        lang_menu.add_command(label="English", command=lambda: self.cambiar_idioma('EN'))
        self.lang_menu_button.pack(side="right", padx=10)

        frame_inputs = tk.Frame(self.root, bg="#2E3440", pady=5)
        frame_inputs.pack(fill="x", padx=20)
        frame_inputs.columnconfigure(1, weight=1)

        self.label_prefijo = tk.Label(frame_inputs, text=text_data[self.current_lang]['prefijo'], bg="#2E3440", fg="#D8DEE9", font=fuente_label)
        self.label_prefijo.grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_prefijo = tk.Entry(frame_inputs, font=fuente_entry, bg="#ECEFF4", fg="#2E3440")
        self.entry_prefijo.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        self.label_inicio = tk.Label(frame_inputs, text=text_data[self.current_lang]['inicio'], bg="#2E3440", fg="#D8DEE9", font=fuente_label)
        self.label_inicio.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_inicio = tk.Entry(frame_inputs, font=fuente_entry, bg="#ECEFF4", fg="#2E3440")
        self.entry_inicio.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        self.label_fin = tk.Label(frame_inputs, text=text_data[self.current_lang]['fin'], bg="#2E3440", fg="#D8DEE9", font=fuente_label)
        self.label_fin.grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.entry_fin = tk.Entry(frame_inputs, font=fuente_entry, bg="#ECEFF4", fg="#2E3440")
        self.entry_fin.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        self.label_repeticiones = tk.Label(frame_inputs, text=text_data[self.current_lang]['repeticiones'], bg="#2E3440", fg="#D8DEE9", font=fuente_label)
        self.label_repeticiones.grid(row=3, column=0, sticky="e", padx=5, pady=5)
        repeticiones_var = tk.StringVar(value="1")
        self.entry_repeticiones = tk.Spinbox(
            frame_inputs, 
            from_=0, 
            to=100, 
            textvariable=repeticiones_var, 
            font=fuente_entry, 
            bg="#ECEFF4", 
            fg="#2E3440",
            width=5
        )
        self.entry_repeticiones.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        frame_botones = tk.Frame(self.root, bg="#2E3440")
        frame_botones.pack(pady=(0, 10))

        self.btn_buscar_texto = tk.Button(frame_botones, text=text_data[self.current_lang]['buscar_texto'], font=fuente_btn, bg="#81A1C1", fg="#2E3440", relief="raised", bd=3, command=self.buscar_desde_texto, padx=10)
        self.btn_buscar_texto.grid(row=0, column=0, padx=5, pady=10)
        self.hover(self.btn_buscar_texto, "#5E81AC", "#81A1C1")

        self.btn_buscar_archivo = tk.Button(frame_botones, text=text_data[self.current_lang]['buscar_archivo'], font=fuente_btn, bg="#D08770", fg="#2E3440", relief="raised", bd=3, command=self.buscar_desde_archivo, padx=10)
        self.btn_buscar_archivo.grid(row=0, column=1, padx=5, pady=10)
        self.hover(self.btn_buscar_archivo, "#BF616A", "#D08770")

        self.btn_copiar = tk.Button(frame_botones, text=text_data[self.current_lang]['copiar'], font=fuente_btn, bg="#A3BE8C", fg="#2E3440", relief="raised", bd=3, command=self.copiar_resultados, padx=10)
        self.btn_copiar.grid(row=0, column=2, padx=5, pady=10)
        self.hover(self.btn_copiar, "#8FBCBB", "#A3BE8C")
        self.btn_copiar.grid_remove()

        self.resultado_text = scrolledtext.ScrolledText(
            self.root, 
            font=fuente_text, 
            bg="#ECEFF4", 
            fg="#2E3440", 
            wrap=tk.WORD,
            undo=True
        )
        self.resultado_text.pack(fill="both", expand=True, padx=20, pady=10)

    def cambiar_idioma(self, lang):
        self.current_lang = lang
        lang_texts = text_data[self.current_lang]
        
        self.root.title(lang_texts['title'])
        self.lang_menu_button.config(text=lang_texts['idioma'])
        self.label_prefijo.config(text=lang_texts['prefijo'])
        self.label_inicio.config(text=lang_texts['inicio'])
        self.label_fin.config(text=lang_texts['fin'])
        self.label_repeticiones.config(text=lang_texts['repeticiones'])
        self.btn_buscar_texto.config(text=lang_texts['buscar_texto'])
        self.btn_buscar_archivo.config(text=lang_texts['buscar_archivo'])
        self.btn_copiar.config(text=lang_texts['copiar'])

    def realizar_busqueda(self, texto_a_buscar):
        self.resultado_text.delete(1.0, tk.END) 
        lang_texts = text_data[self.current_lang]

        if not texto_a_buscar.strip():
            messagebox.showwarning(lang_texts['vacio_title'], lang_texts['vacio_msg'])
            return

        try:
            prefijo = self.entry_prefijo.get().strip()
            inicio = int(self.entry_inicio.get())
            fin = int(self.entry_fin.get())
            repeticiones = int(self.entry_repeticiones.get())
        except ValueError:
            messagebox.showerror(lang_texts['error_title'], lang_texts['error_datos_msg'])
            return

        faltantes = encontrar_faltantes(texto_a_buscar, prefijo, inicio, fin, repeticiones)

        if faltantes:
            cantidad_faltantes = len(faltantes)
            if repeticiones < 2:
                encabezado = lang_texts['faltantes_msg'].format(cantidad=cantidad_faltantes)
            else:
                encabezado = lang_texts['menos_rep_msg'].format(cantidad=cantidad_faltantes, repeticiones=repeticiones)
            
            self.resultado_text.insert(tk.END, encabezado + ", ".join(faltantes))
            self.btn_copiar.grid()  
            self.label_gif.place_forget()
        else:
            self.resultado_text.insert(tk.END, lang_texts['perfecto_msg'])
            self.btn_copiar.grid_remove()
            self.mostrar_gif()

    def buscar_desde_texto(self):
        texto = self.resultado_text.get("1.0", tk.END)
        self.realizar_busqueda(texto)

    def buscar_desde_archivo(self):
        lang_texts = text_data[self.current_lang]
        archivo = filedialog.askopenfilename(
            title=lang_texts['select_file_title'], 
            filetypes=[(lang_texts['text_files'], "*.txt")]
        )
        if not archivo:
            return
        
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                texto = f.read()
            self.realizar_busqueda(texto)
        except Exception as e:
            messagebox.showerror(lang_texts['file_error_title'], lang_texts['file_error_msg'].format(e=e))

    def copiar_resultados(self):
        lang_texts = text_data[self.current_lang]
        self.root.clipboard_clear()
        self.root.clipboard_append(self.resultado_text.get(1.0, tk.END).strip())
        messagebox.showinfo(lang_texts['copiado_title'], lang_texts['copiado_msg'])

    def hover(self, btn, color_hover, color_normal):
        btn.bind("<Enter>", lambda e: btn.config(bg=color_hover))
        btn.bind("<Leave>", lambda e: btn.config(bg=color_normal))

    def mostrar_gif(self):
        self.root.update_idletasks()
        try:
            x = self.resultado_text.winfo_x() + self.resultado_text.winfo_width() - 305
            y = self.resultado_text.winfo_y() + self.resultado_text.winfo_height() + 50
            self.label_gif.place(x=x, y=y)
            self.animar_gif()
        except Exception as e:
            print(f"Error al posicionar GIF: {e}. Usando fallback.")
            self.label_gif.place(x=200, y=200)
            self.animar_gif()

    def animar_gif(self, ind=0):
        if not hasattr(self.label_gif, 'frames') or not self.label_gif.frames:
            return
        frame = self.label_gif.frames[ind]
        self.label_gif.config(image=frame)
        ind = (ind + 1) % len(self.label_gif.frames)
        self.root.after(self.delay, self.animar_gif, ind)
