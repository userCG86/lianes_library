import pandas as pd
import db


def create_friend(name, max_loans=2, notes=None):
    engine = db.get_engine()
    df = pd.DataFrame(
        [[name, max_loans, notes]],
        columns=["name", "max_loans", "notes"]
    )
    df.to_sql(
        "friends", 
        if_exists="append", 
        con=engine, 
        index=False
    )
    message = f"Added '{name}' to 'friends'."
    
    return message

def create_book(title, isbn, author=None, genre=None):
    engine = db.get_engine()
    df = pd.DataFrame(
        [[title, author, genre, isbn]], 
        columns=["title", "author", "genre", "isbn"]
    )
    df.to_sql(
        "books",
        if_exists="append", 
        con=engine, 
        index=False
    )
    message = f"Added '{title}' to 'books'."
        
    return message

def create_loan(friend, book, loan_date=pd.Timestamp.today().date(), next_contact=pd.Timestamp.today().date() + pd.Timedelta(30, "d"), notes=None):
    engine = db.get_engine()
    df = pd.DataFrame(
        [[book["isbn"], friend["friend_id"], loan_date, next_contact, notes]],
        columns = ["isbn", "friend_id", "loan_date", "next_contact", "notes"]
    )
    df.to_sql(
        "loans",
        if_exists="append",
        con=engine,
        index=False
    )
    message = f"Added '{friend["name"]}' borrowed '{book["title"]}' to 'loans'."

    return message
