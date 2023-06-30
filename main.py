import tkinter as tk
from tkinter import ttk
from tkinter import *
import pandas as pd

# constant variables for common colours
WHITE='#FFFFFF'
BLACK='#000000'

class App(tk.Tk):
    def __init__(self):
        # Calls the initialization method of the parent class 'tk.Tk'
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

        # create instance of DataTable class
        self.data_table = DataTable(self)
        # placing DataTable on screen
        self.data_table.place(relx=0.2, rely=0.15, relheight=0.7, relwidth=0.7)
        # creating pandas DataFrame from csv file, then passing DataFrame to DataTable
        self.data_table.set_datatable(pd.read_csv('employee_data.csv'))

    # define export button click function
    def export_button_click(self):
            print('Export Button clicked')

    # define import button click function
    def import_button_click(self):
            print('Import Button clicked')


# Defining a class to represent a csv as a table on screen
class DataTable(ttk.Treeview):
    # The initialising method for class, which takes a parent tkinter class as input
    def __init__(self, parent):
        # Calls the initialization method of the parent class 'ttk.Treeview'
        super().__init__(parent)
        style = ttk.Style()
        scroll_Y = ttk.Scrollbar(parent, orient=tk.HORIZONTAL, command=self.yview)
        style.configure(scroll_Y, background=WHITE, arrowcolour=WHITE, bordercolour=BLACK)
        scroll_X = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.xview)
        style.configure(scroll_X, background=WHITE, arrowcolour=WHITE, bordercolour=BLACK)
        scroll_Y.pack(side=tk.RIGHT, fill=BOTH)
        scroll_X.pack(side=tk.BOTTOM, fill=BOTH)
        # Configures the Treeview to use the scrollbars for their respective views
        self.configure(yscrollcommand=scroll_Y.set, xscrollcommand=scroll_X.set)
        self.stored_dataframe = pd.DataFrame()

    def set_datatable(self, dataframe):
        # Stores the provided dataframe
        self.stored_dataframe = dataframe
        # Draws the table with the data from the dataframe
        self._draw_table(dataframe)

    def _draw_table(self, dataframe):
        # Deletes all existing children nodes in the Treeview (clearing old data)
        self.delete(*self.get_children())
        # Gets the column names from the dataframe
        columns = list(dataframe.columns)
        # Sets the columns of the Treeview to be the column names from the dataframe
        self["columns"] = columns
         # Configures the Treeview to display column headings
        self["show"] = "headings"

        # Iterates over each column, setting the TreeViews's column heading to the column name  
        for col in columns:
            self.heading(col, text=col)

        # Gets the data rows from the dataframe as a list of lists
        df_rows = dataframe.to_numpy().tolist()
        # Iterates over each row, inserting the row into the Treeview
        for row in df_rows:
            self.insert("", "end", values=row)
        return None


if __name__ == "__main__":
    app = App()
    app.mainloop()