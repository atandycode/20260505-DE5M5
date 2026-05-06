import pandas as pd
import argparse

class DataSetCleaner:
    def __init__(self):

        self.df_book_cols = {
            'Id': 'ID',
            'Books': 'Title',
            'Book checkout': 'Checkout',
            'Book Returned': 'Returned',
            'Days allowed to borrow': 'Week_Allowance',
            'Customer ID': 'Cust_ID'
        }

        self.df_customers_cols = {
            'Customer ID': 'ID',
            'Customer Name': 'Name'
        }

        # self.books_input = books_input
        # self.books_output = books_output
        # self.customers_input = customers_input
        # self.customers_output = customers_output


    def open_csv_file_as_dataframe(self, file_loc):
        df = pd.read_csv(file_loc)
        return df

    def drop_empty_rows_from_df(self, df):
        df = df.dropna(how='all')
        return df.reset_index(drop=True)

    def rename_df_cols(self, df, col_dict):
        df = df.rename(columns=col_dict)
        return df

    def enforce_ID_as_integer(self, df):
        df['ID'] = df['ID'].fillna(0).astype(int)
        return df

    def clean_dataframe_basic(self, df, col_dict):
        df = self.rename_df_cols(df, col_dict)
        df = self.drop_empty_rows_from_df(df)
        df = self.enforce_ID_as_integer(df)
        return df

    def clean_book_titles(self, df_title_col):
        df_title_col = df_title_col.fillna('Missing Book Title').astype(str)
        df_title_col = df_title_col.str.strip()
        return df_title_col.str.title()

    def clean_book_dates(self, df_date_col):
        df_date_col = df_date_col.str.replace(r'[^0-9/\-\.]', '', regex=True)
        df_date_col = pd.to_datetime(df_date_col, errors='coerce', dayfirst=True)
        return df_date_col.fillna(pd.NaT)

    def clean_book_week_allowance(self, df_allowance_col):
        df_allowance_col = df_allowance_col.str.replace(r'[^0-9]', '', regex=True)
        df_allowance_col = df_allowance_col.str.strip()
        return df_allowance_col.fillna(0).astype(int)

    def clean_cust_id(self, df_custid_col):
        df_custid_col = df_custid_col.fillna(0).astype(int)
        return df_custid_col

    def clean_book_dataframe(self, df):
        df['Title'] = self.clean_book_titles(df['Title'])
        df['Checkout'] = self.clean_book_dates(df['Checkout'])
        df['Returned'] = self.clean_book_dates(df['Returned'])
        df['Week_Allowance'] = self.clean_book_week_allowance(df['Week_Allowance'])
        df['Cust_ID'] = self.clean_cust_id(df['Cust_ID'])
        return df

    def average_book_checkout_per_cust(self, df):
        df['Book_Checkout_Days'] = (df['Returned'] - df['Checkout']).dt.days
        avg_checkout = df.groupby('Cust_ID')['Book_Checkout_Days'].mean().reset_index()
        avg_checkout.columns = ['ID', 'Avg_Checkout_Days']
        avg_checkout['Avg_Checkout_Days'].round(1)
        return avg_checkout

    def enrich_data(self, df_book, df_customers):
        avg_checkout = self.average_book_checkout_per_cust(df_book)
        df_customers = df_customers.merge(avg_checkout, on='ID', how='left')
        return df_customers

    def main(self):
        # Open datasets into dataframes
        df_book = self.open_csv_file_as_dataframe('./Data/03_LibrarySystemBook.csv')
        df_customers = self.open_csv_file_as_dataframe('./Data/03_LibrarySystemCustomers.csv')

        # Run basic dataframe cleaning on both sets
        df_book = self.clean_dataframe_basic(df_book, self.df_book_cols)
        df_customers = self.clean_dataframe_basic(df_customers, self.df_customers_cols)

        # Run data set specific cleaning
        df_book = self.clean_book_dataframe(df_book)

        # Enrich dataset
        df_customers = self.enrich_data(df_book, df_customers)

        # Output datasets to csv files ready for SQL import
        df_book.to_csv('./data/cleaned_library_system_books.csv', index=False)
        df_customers.to_csv('./data/cleaned_library_system_customers.csv', index=False)

if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description="Cleaning Datasets")

    # parser.add_argument('--books_input', type=str, required=True, help = 'Path to books CSV dataset')
    # parser.add_argument('--customers_input', type=str, required=True, help = 'Path to customers CSV dataset')

    # args = parser.parse_args()
    
    main = DataSetCleaner()
    main.main()