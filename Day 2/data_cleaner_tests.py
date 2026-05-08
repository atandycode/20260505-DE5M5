import unittest
from main import DataSetCleaner
import pandas as pd
import pandas.testing as pdt

class TestOperations(unittest.TestCase):
    def setUp(self):
        self.df_invalid_dataset = pd.read_csv('./Data/03_LibrarySystemBook.csv')
        self.col_dict_books = {
            'Id': 'ID',
            'Books': 'Title',
            'Book checkout': 'Checkout',
            'Book Returned': 'Returned',
            'Days allowed to borrow': 'Week_Allowance',
            'Customer ID': 'Cust_ID'
        }

        # Load CSV
        self.Cleaner = DataSetCleaner()
        self.df = self.Cleaner.open_csv_file_as_dataframe(file_loc='./Data/03_LibrarySystemBook.csv')

    def test_loadCSV(self):
        df_csv = pd.read_csv('./Data/03_LibrarySystemBook.csv')
        pdt.assert_frame_equal(self.df, df_csv)
   
    def test_drop_empty_rows(self):
        total_rows = self.df_invalid_dataset.all(axis=1).sum()
        empty_rows = self.df_invalid_dataset.isna().all(axis=1).sum()
        
        process_rows = self.Cleaner.drop_empty_rows_from_df(self, self.df_invalid_dataset)

        self.assertEqual(process_rows.all(axis=1).sum(), total_rows - empty_rows, "Total dropped rows don't match.")

    def test_rename_df_cols(self):
        process_cols = DataSetCleaner.rename_df_cols(self, self.df_invalid_dataset, self.col_dict_books)
        col_list = list(self.col_dict_books.values())
        col_titles = process_cols.columns.tolist()

        self.assertEqual(col_titles, col_list, "Column titles don't match.")

    def test_enforce_ID_as_integer(self):
        df_clean = DataSetCleaner.rename_df_cols(self, self.df_invalid_dataset, self.col_dict_books)
        process_IDs = DataSetCleaner.enforce_ID_as_integer(self, df_clean)

        self.assertTrue(pd.api.types.is_integer_dtype(process_IDs['ID']))

    def test_clean_book_titles(self):
        process_titles = DataSetCleaner.clean_book_titles(self, self.df_invalid_dataset['Books'])

        self.assertEqual(process_titles[0], 'Catcher In The Rye', "Book title not cleaned.")

    def test_clean_book_dates(self):
        process_dates = DataSetCleaner.clean_book_dates(self, self.df_invalid_dataset['Book checkout'])

        self.assertTrue(pd.api.types.is_datetime64_dtype(process_dates))

    def test_clean_book_allowance(self):
        process_allowance = DataSetCleaner.clean_book_week_allowance(self, self.df_invalid_dataset['Days allowed to borrow'])

        self.assertTrue(pd.api.types.is_integer_dtype(process_allowance))

    def test_clean_cust_id(self):
        pass

    def test_avg_book_checkout(self):
        df_clean = DataSetCleaner.clean_dataframe_basic(self, self.df_invalid_dataset, self.col_dict_books)
        df_clean2 = DataSetCleaner.clean_book_dataframe(self, df_clean)
        
        process_avg_book_checkout = DataSetCleaner.average_book_checkout_per_cust(self, df_clean2)

        self.assertEqual(process_avg_book_checkout[1], 5.0, "Average checkout days don't match")

    def test_enrich_data(self):
        pass




if __name__ == "__main__":
    unittest.main()