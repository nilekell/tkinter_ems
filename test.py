import unittest
from unittest.mock import Mock, patch
import pandas as pd
from tkinter import *
import tkinter as tk
from tkinter import ttk
from main import App
from main import DataTable

class TestAppMethods(unittest.TestCase):

    def setUp(self):
        # called before each test method is executed.
        app = App()
        app.mainloop()

    # patch is a decorator that's replacing the normal 'pandas.DataFrame.to_csv' method
    # and 'app.App.data_table.get_datatable' method with a mock (or fake) one
    # This allows us to control their behavior for testing
    @patch('pandas.DataFrame.to_csv')
    @patch('app.App.data_table.get_datatable', return_value=pd.DataFrame())
    def test_export_button_click(self, mock_get_datatable, mock_to_csv):
        # call the export_button_click method on the app instance
        self.app.export_button_click()
        # checks that the mock_get_datatable was called exactly once
        mock_get_datatable.assert_called_once()
        # checks that the mock_to_csv was called exactly once
        mock_to_csv.assert_called_once()

    # Similar to the first test method, these patches replace 'pandas.read_csv' and 'app.App.data_table.set_datatable' 
    # methods with mocks.
    @patch('pandas.read_csv', return_value=pd.DataFrame())
    @patch('app.App.data_table.set_datatable')
    def test_import_button_click(self, mock_set_datatable, mock_read_csv):
        # call the import_button_click method on the app instance
        self.app.import_button_click()
        # checks that the mock_read_csv was called exactly once with 'employee_data.csv'
        mock_read_csv.assert_called_once_with('employee_data.csv')
        # checks that the mock_set_datatable was called exactly once
        mock_set_datatable.assert_called_once()


class TestDataTable(unittest.TestCase):

    def setUp(self):
        # creating a root tkinter window
        self.root=tk.Tk()
        # creating an instance of DataTable class under tk.Tk()
        self.data_table = DataTable(self.root)
        # creating a simple mock pandas DataFrame instance
        self.test_df = pd.DataFrame({'column1': [1, 2, 3], 'column2': ['a', 'b', 'c']})
        # assigning the mock DataFrame to the DataTable attribute: stored_dataframe
        self.data_table.set_datatable(self.test_df)

    def test_get_datatable(self):
        # Here we are manually setting the 'stored_dataframe' attribute of our DataTable instance
        # to a known DataFrame 'self.test_df' that we created for testing. 
        # This step is essentially simulating the behavior of the 'set_datatable' method.
        self.data_table.stored_dataframe = self.test_df
        # Now we are returning the DataFrame currently stored in the DataTable ('self.test_df')
        result_df = self.data_table.get_datatable()
        # Chcking if the DataFrame returned by 'get_datatable' is identical to the 
        #  DataFrame that we stored in the DataTable instance.
        pd.testing.assert_frame_equal(self.test_df, result_df)

    def test_update_data(self):
        # Retrieving the mock DataFrame instane to simulate initial state of DataTable
        self.data_table.stored_dataframe = self.test_df
        # the cell at index 1 and column 'column1' is to be updated 
        # with the value 'value1'.
        self.data_table.update_data(1, 'value1', 'column1', 'value1')
        # Checking that the update was successful
        # The cell at index 1 and column 'column1' of the stored_dataframe attribute of the DataTable 
        # instance should now contain the value 'value1'.
        self.assertEqual(self.data_table.stored_dataframe.loc[1, 'column1'], 'value1')

    def test_set_datatable(self):
        # assigning the mock DataFrame to the DataTable attribute: stored_dataframe
        self.data_table.set_datatable(self.test_df)
        # Now we are returning the DataFrame currently stored in the DataTable ('self.test_df')
        result_df = self.data_table.get_datatable()
        # Checking if the set mock DataFrame is equal to the DataFrame returned from 'get_datatable()'
        pd.testing.assert_frame_equal(self.test_df, result_df)

    def tearDown(self):
        # Destroying all tkinter widgets once all tests have been complete
        self.root.destroy()


if __name__ == '__main__':
    unittest.main()
