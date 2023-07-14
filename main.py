import tkinter as tk
from tkinter import ttk
from tkinter import *
import pandas as pd
import random
from random import randint

# NEED TO WRITE CHANGES TO employee_data.csv in save_data()
# NEED TO EXPORT A COPY OF employee_data.csv with a new name

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
        self.export_button.place(relx=0.07, rely=0.17)

        # create the second button with text 'Import Data'
        self.import_button = tk.Button(self, text='Import Data', command=self.import_button_click, height=self.button_size, width=self.button_size, relief='solid', borderwidth=2)
        self.import_button.place(relx=0.07, rely=0.37) 

        # creat the third button with text 'Edit Data'
        self.edit_button = tk.Button(self, text='Edit Data', command=self.edit_button_click, height=self.button_size, width=self.button_size, relief='solid', borderwidth=2)
        self.edit_button.place(relx=0.07, rely=0.57)

        # create instance of DataTable class
        self.data_table = DataTable(self)
        # grid DataTable inside the frame
        self.data_table.grid(row=0, column=0, sticky='nsew')
        # placing DataTable on screen
        self.data_table.place(relx=0.2, rely=0.15, relheight=0.7, relwidth=0.7)
        # creating pandas DataFrame from csv file, then passing DataFrame to DataTable
        self.data_table.set_datatable(pd.read_csv('employee_data.csv'))

    # define export button click function
    def export_button_click(self):
        # Get the current DataFrame from the data_table object
        current_df = self.data_table.get_datatable()
        filename = f"updated_employee_data_{randint(100, 999)}.csv"
        # Write the DataFrame to a new CSV file
        current_df.to_csv(filename, index=False)

        print(f"{filename} saved to current working directory")

    # define import button click function
    def import_button_click(self):
        print('Import Button clicked')

    def edit_button_click(self):
        selected_item = self.data_table.selection() # gets the selected item
        if len(selected_item) == 0:
            print('No record in the table is selected')

        if selected_item:  # if something is selected
            row_values = self.data_table.item(selected_item[0])["values"]  # gets the values of the selected item
            column_names = self.data_table["columns"]  # gets the columns of the datatable
            row_index = self.data_table.get_children().index(selected_item[0]) # gets the index of the selected row in datatable
            EditWindow(self, row_values, column_names, selected_item[0], row_index)  # opens a new window with the selected item's data
         
class EditWindow(tk.Toplevel):
    def __init__(self, parent, row_values, column_names, selected_id, row_index):  

        super().__init__(parent)
        self.parent = parent
        self.row_index = row_index # index of the selected row in the datatable
        self.row_values = row_values # values for each column in datatable
        self.column_names = column_names # columns of the datatable
        self.selected_id = selected_id # unique id of selected record in database
        self.geometry('500x500') # setting size of pop edit window
        self.title('Edit Record') # setting title of edit window
        self.entries = [] # initialising empty list to store
        
        # enumerate() creates an Iterable object that generates a tuple for each iteration, where the 
        # first value is the index and the second value is the actual value from 'row_values'
        # e.g. in the first iteration, the tuple will be: {0, Name}, 
        # in the second iteration, the tuple will be {1, Job Title} etc
        for i, value in enumerate(row_values):
            tk.Label(self, text=column_names[i]).grid(row=i, column=0)  # create a label for each column
            entry = tk.Entry(self)  # create entry for each column
            entry.grid(row=i, column=1)  # add entry to grid
            entry.insert(0, value)  # add existing value to the entry
            self.entries.append(entry)  # append entry to entries list

        tk.Button(self, text='Save', command=self.save_data).grid(row=len(row_values), column=0, columnspan=2)  # create save button

    def save_data(self):
        # 'enumerate' is used to get both the index 'i' and the value 'entry' in each iteration.
        for i, entry in enumerate(self.entries):
            # For the current entry, we call the 'get' method to retrieve the value from the entry field. 
            # An Entry is a basic Tkinter widget to input text. The 'get' method is used to fetch the text that has been input.
            entry_value = entry.get()

            # We retrieve the column name for the current entry from 'self.column_names' using 'i' as the index. 
            # 'self.column_names' is a list of column names, and 'i' corresponds to the current entry's position in these columns.
            column_name = self.column_names[i]

            # Now we update the value of the specific cell in the DataTable. 
            # 'self.row_index' represents the index of the row being edited.
            # 'column_name' is the column where the current entry resides. 
            # 'entry_value' is the new value for this cell.
            #  update_data() is used to update datatable with entry data
            self.parent.data_table.update_data(self.row_index, self.selected_id, column=column_name, value=entry_value)

        self.parent.data_table.stored_dataframe.to_csv('employee_data.csv', index=False)
        
        self.destroy()  # close window


# Defining a class to represent a csv as a table on screen
class DataTable(ttk.Treeview):
    # The initialising method for class, which takes a parent tkinter class as input
    def __init__(self, parent):
        # Calls the initialization method of the parent class 'ttk.Treeview'
        super().__init__(parent)
        # Create a grid layout for parent
        parent.grid()

        style = ttk.Style()

        # Scrollbars only show if there are enough rows/columns to overflow DataTable 

        # Create vertical scrollbar
        scroll_Y = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.yview)
        style.configure("Vertical.TScrollbar", background=WHITE, arrowcolour=WHITE, bordercolour=BLACK)
        scroll_Y.grid(row=0, column=1, sticky='ns')  # Grid vertical scrollbar to the right of the Treeview

        # Create horizontal scrollbar
        scroll_X = ttk.Scrollbar(parent, orient=tk.HORIZONTAL, command=self.xview)
        style.configure("Horizontal.TScrollbar", background=WHITE, arrowcolour=WHITE, bordercolour=BLACK)
        scroll_X.grid(row=1, column=0, sticky='ew')  # Grid horizontal scrollbar below the Treeview

        # Allow the Treeview to expand
        parent.grid_columnconfigure(0, weight=1)  # Allows Treeview to expand horizontally
        parent.grid_rowconfigure(0, weight=1)  # Allows Treeview to expand vertically

        # Configure the Treeview to use the scrollbars
        self.configure(yscrollcommand=scroll_Y.set, xscrollcommand=scroll_X.set)
        # Place Treeview in the grid
        self.grid(row=0, column=0, sticky="nsew")

        self.stored_dataframe = pd.DataFrame()


    def get_datatable(self):
        return self.stored_dataframe
    
    def update_data(self, index, item, column=None, value=None):
        # This updates the value in the displayed data table
        if column is not None:
            item = self.get_children()[index]
            current_values = list(self.item(item, 'values'))
            current_values[self['columns'].index(column)] = value
            self.item(item, values=current_values)
        
        # This updates the value in the stored dataframe
        if self.stored_dataframe is not None and column in self.stored_dataframe.columns:
            self.stored_dataframe.loc[index, column] = value

    def set_datatable(self, dataframe):
        # Stores the provided dataframe
        self.stored_dataframe = dataframe.reset_index(drop=True)
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