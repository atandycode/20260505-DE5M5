import pandas as pd
import argparse

def open_csv_file_as_dataframe(file_loc):
    df = pd.read_csv(file_loc)
    return df

def drop_empty_rows_from_df(df):
    df = df.dropna(how='all')
    return df.reset_index(drop=True)

def rename_df_cols(df, col_dict):
    df = df.rename(columns=col_dict)
    return df

def enforce_ID_as_integer(df):
    df['ID'] = df['ID'].fillna(0).astype(int)
    return df

def clean_dataframe_basic(df, col_dict):
    df = rename_df_cols(df, col_dict)
    df = drop_empty_rows_from_df(df)
    df = enforce_ID_as_integer(df)
    return df

def clean_book_titles(df_title_col):
    df_title_col = df_title_col.fillna('Missing Book Title').astype(str)
    df_title_col = df_title_col.str.strip()
    return df_title_col.str.title()

def clean_book_dates(df_date_col):
    df_date_col = df_date_col.str.replace(r'[^0-9/\-\.]', '', regex=True)
    df_date_col = pd.to_datetime(df_date_col, errors='coerce', dayfirst=True)
    return df_date_col.fillna(pd.NaT)

def clean_book_week_allowance(df_allowance_col):
    df_allowance_col = df_allowance_col.str.replace(r'[^0-9]', '', regex=True)
    df_allowance_col = df_allowance_col.str.strip()
    return df_allowance_col.fillna(0).astype(int)

def clean_cust_id(df_custid_col):
    df_custid_col = df_custid_col.fillna(0).astype(int)
    return df_custid_col

def clean_book_dataframe(df):
    df['Title'] = clean_book_titles(df['Title'])
    df['Checkout'] = clean_book_dates(df['Checkout'])
    df['Returned'] = clean_book_dates(df['Returned'])
    df['Week_Allowance'] = clean_book_week_allowance(df['Week_Allowance'])
    df['Cust_ID'] = clean_cust_id(df['Cust_ID'])
    return df

def average_book_checkout_per_cust(df):
    df['Book_Checkout_Days'] = (df['Returned'] - df['Checkout']).dt.days
    avg_checkout = df.groupby('Cust_ID')['Book_Checkout_Days'].mean().reset_index()
    avg_checkout.columns = ['ID', 'Avg_Checkout_Days']
    avg_checkout['Avg_Checkout_Days'].round(1)
    return avg_checkout

def enrich_data(df_book, df_customers):
    avg_checkout = average_book_checkout_per_cust(df_book)
    df_customers = df_customers.merge(avg_checkout, on='ID', how='left')
    return df_customers

df_book_cols = {
    'Id': 'ID',
    'Books': 'Title',
    'Book checkout': 'Checkout',
    'Book Returned': 'Returned',
    'Days allowed to borrow': 'Week_Allowance',
    'Customer ID': 'Cust_ID'
}

df_customers_cols = {
    'Customer ID': 'ID',
    'Customer Name': 'Name'
}

def main(args):
    # Open datasets into dataframes
    df_book = open_csv_file_as_dataframe(args.books_input)
    df_customers = open_csv_file_as_dataframe(args.customers_input)

    # Run basic dataframe cleaning on both sets
    df_book = clean_dataframe_basic(df_book, df_book_cols)
    df_customers = clean_dataframe_basic(df_customers, df_customers_cols)

    # Run data set specific cleaning
    df_book = clean_book_dataframe(df_book)

    # Enrich dataset
    df_customers = enrich_data(df_book, df_customers)

    # Output datasets to csv files ready for SQL import
    df_book.to_csv('./data/cleaned_library_system_books.csv', index=False)
    df_customers.to_csv('./data/cleaned_library_system_customers.csv', index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Cleaning Datasets")

    parser.add_argument('--books_input', type=str, required=True, help = 'Path to books CSV dataset')
    parser.add_argument('--customers_input', type=str, required=True, help = 'Path to customers CSV dataset')

    args = parser.parse_args()
    main(args)