import tkinter as tk
from src.GUI import CacheSimulatorGUI  # Adjust import path

if __name__ == "__main__":
    root = tk.Tk()
    app = CacheSimulatorGUI(root)
    root.mainloop()
