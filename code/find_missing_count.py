import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from PIL import Image, ImageTk, ImageSequence
import re, sys, os


if getattr(sys, 'frozen', False):
    BASE_PATH = sys._MEIPASS 
else:
    BASE_PATH = os.path.dirname(__file__)

# --- Path de archivos ---
gif_path = os.path.join(BASE_PATH, "../resources/meme.gif")
icon_path = os.path.join(BASE_PATH, "../resources/icono.ico")

# --- Funciones ---
def buscar_faltantes():
    archivo = filedialog.askopenfilename(title="Seleccionar archivo", filetypes=[("Text files", "*.txt")])
    if not archivo:
        return

    prefijo = entry_prefijo.get().strip()
    try:
        inicio = int(entry_inicio.get())
        fin = int(entry_fin.get())
    except ValueError:
        messagebox.showerror("Error", "El valor inicial y final deben ser números enteros")
        return

    with open(archivo, "r", encoding="utf-8") as f:
        texto = f.read()

    patron = re.escape(prefijo) + r"(\d+)" if prefijo else r"(\d+)"
    encontrados = re.findall(patron, texto)
    numeros_encontrados = set(int(n) for n in encontrados)

    faltantes = [f"{prefijo}{n}" for n in range(inicio, fin + 1) if n not in numeros_encontrados]

    resultado_text.config(state="normal")
    resultado_text.delete(1.0, tk.END)
    if faltantes:
        resultado_text.insert(tk.END, "Faltan estos números:\n" + ", ".join(faltantes))
        btn_copiar.grid()  
        label_gif.place_forget()
    else:
        resultado_text.insert(tk.END, "No faltan números en el rango indicado.")
        btn_copiar.grid_remove()
        mostrar_gif()
    resultado_text.config(state="disabled")

def copiar_resultados():
    root.clipboard_clear()
    root.clipboard_append(resultado_text.get(1.0, tk.END).strip())
    messagebox.showinfo("Copiado", "Resultados copiados al portapapeles")

# --- Hover Ef ---
def hover(btn, color_hover, color_normal):
    btn.bind("<Enter>", lambda e: btn.config(bg=color_hover))
    btn.bind("<Leave>", lambda e: btn.config(bg=color_normal))

# --- Display GIF ---
def mostrar_gif():
    root.update_idletasks()
    x = resultado_text.winfo_x() + resultado_text.winfo_width() - 350
    y = resultado_text.winfo_y() + resultado_text.winfo_height() - 60
    label_gif.place(x=x, y=y)
    animar_gif()

def animar_gif(ind=0):
    frame = label_gif.frames[ind]
    label_gif.config(image=frame)
    ind = (ind + 1) % len(label_gif.frames)
    root.after(delay, animar_gif, ind)

# --- Ventana main ---
root = tk.Tk()
root.title("Buscador de números faltantes")
root.geometry("700x500")
root.minsize(550, 400)
root.configure(bg="#2E3440")

# Asignacion icono
try:
    root.iconbitmap(icon_path)
except Exception as e:
    print(f"No se pudo asignar el ícono: {e}")

fuente_label = ("Segoe UI", 11)
fuente_entry = ("Segoe UI", 11)
fuente_btn = ("Segoe UI", 11, "bold")
fuente_text = ("Consolas", 11)

# --- Frame Inputs ---
frame_inputs = tk.Frame(root, bg="#2E3440", pady=15)
frame_inputs.pack(fill="x", padx=20)
frame_inputs.columnconfigure(1, weight=1)

tk.Label(frame_inputs, text="Prefijo (opcional):", bg="#2E3440", fg="#D8DEE9", font=fuente_label).grid(row=0, column=0, sticky="e", padx=5, pady=5)
entry_prefijo = tk.Entry(frame_inputs, font=fuente_entry, bg="#ECEFF4", fg="#2E3440")
entry_prefijo.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

tk.Label(frame_inputs, text="Valor inicial:", bg="#2E3440", fg="#D8DEE9", font=fuente_label).grid(row=1, column=0, sticky="e", padx=5, pady=5)
entry_inicio = tk.Entry(frame_inputs, font=fuente_entry, bg="#ECEFF4", fg="#2E3440")
entry_inicio.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

tk.Label(frame_inputs, text="Valor final:", bg="#2E3440", fg="#D8DEE9", font=fuente_label).grid(row=2, column=0, sticky="e", padx=5, pady=5)
entry_fin = tk.Entry(frame_inputs, font=fuente_entry, bg="#ECEFF4", fg="#2E3440")
entry_fin.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

# --- Frame Botones ---
frame_botones = tk.Frame(root, bg="#2E3440")
frame_botones.pack(fill="x", padx=20)
frame_botones.columnconfigure(0, weight=1)

btn_buscar = tk.Button(frame_botones, text="  Buscar faltantes", font=fuente_btn, bg="#81A1C1", fg="#2E3440", relief="raised", bd=3, command=buscar_faltantes)
btn_buscar.grid(row=0, column=0, padx=5, pady=10, sticky="w")
hover(btn_buscar, "#5E81AC", "#81A1C1")

btn_copiar = tk.Button(frame_botones, text="  Copiar resultados", font=fuente_btn, bg="#A3BE8C", fg="#2E3440", relief="raised", bd=3, command=copiar_resultados)
btn_copiar.grid(row=0, column=1, padx=5, pady=10, sticky="w")
hover(btn_copiar, "#8FBCBB", "#A3BE8C")
btn_copiar.grid_remove()

# --- RESULTADO ---
resultado_text = scrolledtext.ScrolledText(root, font=fuente_text, bg="#ECEFF4", fg="#2E3440")
resultado_text.pack(fill="both", expand=True, padx=20, pady=10)
resultado_text.config(state="disabled")

# --- GIF ---
try:
    pil_gif = Image.open(gif_path)
    frames = [ImageTk.PhotoImage(frame.copy().convert("RGBA")) for frame in ImageSequence.Iterator(pil_gif)]
    delay = pil_gif.info.get("duration", 100)
    label_gif = tk.Label(root, bg="#2E3440")
    label_gif.frames = frames
except Exception as e:
    print(f"No se pudo cargar el GIF: {e}")
    label_gif = tk.Label(root)

root.mainloop()

