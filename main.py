import tkinter as tk
from tkinter import ttk
from tkinter import *

# constant variables for common colours
WHITE='#FFFFFF'
BLACK='#000000'

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # configure the root window
        self.title("Employee Management System")
        self.geometry('1000x1000')
        self.configure(bg=WHITE)

        # creates a new label with border
        self.title_label = tk.Label(self, text="WORKPLACE EMPLOYEE MANAGEMENT SYSTEM", fg=BLACK, bg=WHITE, font=('Helvetica', 30, 'bold'), relief='solid', borderwidth=5)
        # places the label in a specific place.
        self.title_label.place(relx=0.5, rely=0.05, anchor='center')

        # setting constant button size
        self.button_size = 5

        # create 'Export Data' button
        self.export_button = tk.Button(self, text='Export Data', command=self.export_button_click, height=self.button_size, width=self.button_size, relief='solid', borderwidth=2)
        self.export_button.place(relx=0.07, rely=0.17)  # pack it into the window with some padding

        # create the second button with text 'Import Data'
        self.import_button = tk.Button(self, text='Import Data', command=self.import_button_click, height=self.button_size, width=self.button_size, relief='solid', borderwidth=2)
        self.import_button.place(relx=0.07, rely=0.37)  # pack it into the window with some padding

    # define export button click function
    def export_button_click(self):
            print('Export Button clicked')

    # define import button click function
    def import_button_click(self):
            print('Import Button clicked')
        

if __name__ == "__main__":
    app = App()
    app.mainloop()