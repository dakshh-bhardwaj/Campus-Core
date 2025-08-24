import sys
import customtkinter as ctk


class Loading(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Set window properties
        self.geometry("460x100+500+300")
        self.title("Student Management System")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", lambda: sys.exit())
        ctk.set_appearance_mode("system")  # "light" or "dark"
        ctk.set_default_color_theme("blue")  # Use blue theme
        
        self.screen()
        self.mainloop()

    def screen(self):
        # Add components
        self.label = ctk.CTkLabel(self, text="Loading...", font=("Cambria", 17))
        self.label.place(x=20, y=10)

        self.progressbar = ctk.CTkProgressBar(self, width=400, mode="indeterminate")
        self.progressbar.place(x=20, y=50)
        self.progressbar.start()

        self.after(3110, self.get)  # Trigger get() after 3110 ms

    def get(self):
        self.progressbar.stop()
        self.destroy()


if __name__ == "__main__":
    Loading()
