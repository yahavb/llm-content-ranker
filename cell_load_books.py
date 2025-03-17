# =========================
#  Load Dataset
# =========================
import pandas as pd
import os

books_df_dataset=os.environ['BOOKS_DF_DS']
nrows=os.environ['NROWS']

def load_amazon_books():
    url = "file:///home/ubuntu/Books_rating.csv"  # Adjust if needed
    df = pd.read_csv(url,nrows=int(nrows))
    df = df[['Id', 'Title', 'User_id', 'review/helpfulness', 'review/score', 'review/time', 'review/summary', 'review/text']]
    return df
    
books_df = load_amazon_books()
books_df.to_pickle(books_df_dataset)  
print(f"✅ Books dataset loaded & saved in {books_df_dataset}.")
