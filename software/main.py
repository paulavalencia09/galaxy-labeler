import customtkinter as ctk
from app import GalaxyLabeler

def main():
    ctk.set_appearance_mode("dark")
    app = GalaxyLabeler()
    app.mainloop()


if __name__ == "__main__":
    main()