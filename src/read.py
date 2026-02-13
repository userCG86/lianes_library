import pandas as pd
import db

def prettify_df(df):
    df.columns = [c.upper() if c == "isbn" else c.replace("_", " ").capitalize() for c in df.columns]
    return df.fillna("")

def read_friends():
    engine = db.get_engine()
    return pd.read_sql("friends", con=engine)

def display_friends():
    friends = read_friends()
    return friends.pipe(prettify_df).loc[:, "Name":]

def read_books(available_only=False):
    engine = db.get_engine()
    books = pd.read_sql("books", con=engine)
    if available_only:
        loans = pd.read_sql("loans", con=engine)
        books = pd.merge(books, loans, on="isbn", how="left").query("friend_id.isna()")[books.columns]
    return books

def display_books(available_only=False):
    books = read_books(available_only)
    return books.pipe(prettify_df).sort_values(by="Title")

def read_loans():
    engine = db.get_engine()
    return pd.read_sql("loans", con=engine)

def display_loans():
    friends = read_friends()
    books = read_books()
    loans = read_loans()
    for c in ["loan_date", "last_contact", "next_contact"]:
        loans[c] = loans[c].dt.strftime("%Y-%m-%d")
    
    display_columns = ["title", "name", "loan_date", "last_contact", "next_contact", "notes"]
    df = (
        pd.merge(loans, friends, on="friend_id", suffixes=["", "_no"])
        .merge(books, on="isbn")
        [display_columns]
    )
    return df.pipe(prettify_df).sort_values(by="Loan date")
