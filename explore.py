import pandas as pd

data_source = 'financial_transactions.csv'
def load_data(path):
    df = pd.read_csv(path, low_memory=False)
    return df

def clean_data(df):
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    return df

def validate_data(df):
    print("Shape:", df.shape)
    print("Data types:\n", df.dtypes)
    print("Missing Values:")
    missing = df.isnull().sum()
    if missing.sum() == 0:
        print("No missing values found.\n")
    else:
        print(missing[missing > 0], "\n")
    
    print("Duplicate Rows:")
    dup_count = df.duplicated().sum()
    print(f"Found {dup_count} duplicate rows.\n")
    if dup_count > 0:
        df = df.drop_duplicates()
        print("Dropped duplicates.\n")
    
    if 'transaction_id' in df.columns:
        print("Transaction ID Check:")
        unique_ids = df['transaction_id'].nunique()
        if unique_ids == len(df):
            print("All transaction IDs are unique.\n")
        else:
            print(f"{len(df) - unique_ids} duplicated transaction IDs found.\n")
    
    if 'amount' in df.columns:
        print("Amount Range Check:")
        desc = df['amount'].describe()
        print(desc, "\n")
        
        neg_count = (df['amount'] < 0).sum()
        if neg_count > 0:
            print(f"{neg_count} negative amounts found.\n")
            df = df[df['amount'] >= 0]
            print(df.shape)
        else:
            print("No negative amounts detected.\n")
    
    if 'date' in df.columns:
        print("Date range check:")
        print(f"Min date: {df['date'].min()} , Max date: {df['date'].max()}")
        print(f"Invalid dates: {df['date'].isna().sum()}\n")
    
    print("Categorical columns:")
    categorical_cols = ['category', 'merchant', 'payment_method', 'account_type', 'transaction_type']
    for col in categorical_cols:
        if col in df.columns:
            unique_vals = df[col].dropna().unique()
            print(f"{col} → {len(unique_vals)} unique values")
            vals = [v for v in unique_vals if isinstance(v, str)]
            print("Values:", vals, "\n")
    
    return df

def load_and_prepare(path='financial_transactions.csv'):
    df = load_data(path)
    df = clean_data(df)
    df = validate_data(df)
    return df


