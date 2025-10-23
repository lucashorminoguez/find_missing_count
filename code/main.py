import tkinter as tk
from ui import BuscadorApp

def main():
    root = tk.Tk()
    app = BuscadorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()