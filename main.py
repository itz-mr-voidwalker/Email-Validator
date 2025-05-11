import logging
import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
import re
import sys

class App:
    def __init__(self, root):
        self.root = root
        
        self.setup_logging()
        self.colors = self.define_colors()
        self.window_config()
        self.create_widgets()
               
    def setup_logging(self):
        logging.basicConfig(
            level=logging.DEBUG,
            format= '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers= [
                logging.StreamHandler(),
                logging.FileHandler("app.log", mode='a')
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("App Session Started")
        
    
    
    def define_colors(self):
        """Define and return a modern, sleek dark color scheme for the app."""
        return {
            "bg": "#1E1E2E",
            "fg": "#CDD6F4",
            "entry_bg": "#313244",
            "entry_fg": "#F5E0DC",
            "btn_bg": "#89B4FA",
            "btn_fg": "#1E1E2E",
            "result_fg": "#A6E3A1",
        }




    #Window Configuration
    def window_config(self):
        """Configure the window properties like title, size, and background color."""
        self.root.title("Email Validator")
        self.root.geometry("500x300")
        self.root.resizable(False, False)
        self.root.configure(bg=self.colors["bg"])
        icon_path = 'icon.png'
        if hasattr(sys, '_MEIPASS'):  # This is for the bundled executable
            icon_path = sys._MEIPASS + '/icon.png'
        icon = PhotoImage(file=icon_path)
        self.root.iconphoto(True, icon)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.bind('<Escape>', self.on_closing)
        self.root.bind('<Return>', self.validator)
        
    def on_closing(self, event=None):
        self.logger.info("App Session Over")
        self.root.quit()
        sys.exit()
        
    #Creates Tkinter Widgets
    def create_widgets(self):
        """Create and configure all the necessary widgets for the application."""
        tk.Label(self.root, text="Email Validator", font=('Segoe UI', 20, 'bold'),
                 bg=self.colors["bg"], fg=self.colors["fg"]).pack(pady=20)

        self.entry_box = tk.Entry(self.root, bd=0, width=35, font=('Consolas', 16),
                                  bg=self.colors["entry_bg"], fg=self.colors["entry_fg"],
                                  insertbackground=self.colors["entry_fg"],
                                  highlightthickness=2, highlightbackground="#FFFFFF",
                                  highlightcolor="#FFFFFF")
        self.entry_box.pack(pady=10)
        self.entry_box.focus_set()

        self.result_label = tk.Label(self.root, text="", font=('Consolas', 14),
                                     fg=self.colors["result_fg"], bg=self.colors["bg"])
        self.result_label.pack(pady=30)

        submit_btn = tk.Button(self.root, text="Submit", command= self.validator,
                               bg=self.colors["btn_bg"], fg=self.colors["btn_fg"],
                               font=('Segoe UI', 14), bd=0, activebackground="#81A1C1",
                               activeforeground=self.colors["fg"], padx=20, pady=5)
        submit_btn.pack()

    def validator(self, event=None):
        email = self.entry_box.get().strip()
        
        if not email:
            logging.info("Email Field is Empty")
            self.result_label.config(text="Input Field Can't be Empty", fg='crimson')
            
            return
        
        if self._pattern_matcher(email):
                     
            self.result_label.config(text="✅Email is Valid", fg=[self.colors['result_fg']])
            
            self.logger.info(f"{email} is Valid ")
            return True
        
        self.logger.info(f"The {email} is Invalid")
        self.result_label.config(text="❌ The email is invalid.", fg=[self.colors['result_fg']])           
        return False
        
    def _pattern_matcher(self, email):
        self.email_pattern = r"""
            ^(?!.*\.\.)                             # No double dots
            [a-zA-Z0-9](?:[a-zA-Z0-9._+-]{0,62}[a-zA-Z0-9])?    # Local part
            @
            [a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?       # Domain
            (?:\.[a-zA-Z]{2,10})+$                   # TLD and sub-TLDs
        """
        return True if re.match(self.email_pattern, email, re.VERBOSE) else False

    
    
        
    

def main():
    root = tk.Tk()
    obj = App(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()