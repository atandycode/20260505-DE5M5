import pandas as pd
from datetime import datetime

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
        books_per_customer = df_book.groupby('Cust_ID').agg(total_books =('ID','count' )).reset_index()
        avg_checkout = self.average_book_checkout_per_cust(df_book)
        df_customers = df_customers.merge(avg_checkout, on='ID', how='left')
        df_customers = df_customers.merge(books_per_customer, left_on='ID', right_on='Cust_ID', how='left')
        return df_customers
    
    def generate_metrics(self, df_customers, df_books):
        # Metric 1 - books per customer

        # Combine all metrics into one summary DF

        # return df_metrics
        pass

    def main(self):
        # Create Database and table
        # create_database()


        # Open datasets into dataframes
        df_book = self.open_csv_file_as_dataframe('./data/raw_data/03_LibrarySystemBook.csv')
        df_customers = self.open_csv_file_as_dataframe('./data/raw_data/03_LibrarySystemCustomers.csv')
        
        # Begin timestamp
        start_time = datetime.now()
        cust_rows_before = len(df_customers)
        book_rows_before = len(df_book)

        # Run basic dataframe cleaning on both sets
        df_book = self.clean_dataframe_basic(df_book, self.df_book_cols)
        df_customers = self.clean_dataframe_basic(df_customers, self.df_customers_cols)

        # Run data set specific cleaning
        df_book = self.clean_book_dataframe(df_book)

        cust_rows_after = len(df_customers)
        book_rows_after = len(df_book)
        end_time = datetime.now()

        metrics = {
            'stage': 'clean',
            'customer_rows_before': cust_rows_before,
            'customer_rows_after': cust_rows_after,
            'customer_rows_dropped': cust_rows_before - cust_rows_after,
            'book_rows_before': book_rows_before,
            'book_rows_after': book_rows_after,
            'book_rows_dropped': book_rows_before - book_rows_after,
            'duration_secs': (end_time - start_time).total_seconds(),
            'run_date': start_time.strftime('%Y-%m-%d'),
            'run_time': start_time.strftime('%H:%M:%S')

        }

        pipeline_metrics = []
        pipeline_start = datetime.now()
        pipeline_metrics.append(metrics)

        # Enrich dataset
        df_customers = self.enrich_data(df_book, df_customers)

        # Output datasets to csv files ready for SQL import
        df_book.to_csv('./data/cleaned/cleaned_book_data.csv', index=False)
        df_customers.to_csv('./data/cleaned/cleaned_customers_data.csv', index=False)

        pipeline_metrics.append({
            'stage': 'pipeline_total',
            'rows_before': pipeline_metrics[0].get('rows_before', 0) if pipeline_metrics else 0,
            'rows_after': pipeline_metrics[-1].get('rows_after', 0) if pipeline_metrics else 0,
            'rows_dropped': sum(m.get('rows_dropped', 0) for m in pipeline_metrics),
            'duration_secs': (datetime.now() - pipeline_start).total_seconds(),
            'run_date': pipeline_start.strftime('%Y-%m-%d'),
            'run_time': pipeline_start.strftime('%H:%M:%S')
        })

        df_metrics = pd.DataFrame(pipeline_metrics)
        df_metrics.to_csv('./data/metrics/metrics.csv', index=False)

        print("Pipeline complete!")


        # df_metrics = self.generate_metrics(df_customers, df_book)
        # df_metrics.to_csv('./data/cleaned/metrics.csv', index=False)


        # save_to_database(df_book, 'books')
        # print(df_customers.head().to_csv(index=False))
