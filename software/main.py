import customtkinter as ctk
from app import GalaxyLabeler
import ctypes
import sys

def main():
    ctk.set_appearance_mode("dark")
    if sys.platform == "win32":
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("paulavalencia.galaxylabeler")   
    app = GalaxyLabeler()
    app.mainloop()


if __name__ == "__main__":
    main()