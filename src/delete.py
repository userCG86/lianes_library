import pandas as pd
from sqlalchemy import text
import db

def delete_friend(friend):
    engine = db.get_engine()
    delete_query = f"""DELETE FROM friends
    WHERE friend_id = '{friend["friend_id"]}';"""
    with engine.begin() as connection:
        connection.execute(text(delete_query))
        return f"Removed '{friend['name']}' from 'friends'."

def delete_book(book):
    engine = db.get_engine()
    delete_query = f"""DELETE FROM books
    WHERE isbn = '{book["isbn"]}';"""
    with engine.begin() as connection:
        connection.execute(text(delete_query))
        return f"Removed '{book['title']}' from 'books'."

def delete_loan(loan):
    engine = db.get_engine()
    lookup_table = (pd.read_sql("loans", con=engine).loc[[loan.name]]
                    .merge(pd.read_sql("friends", con=engine), on="friend_id")
                    .merge(pd.read_sql("books", con=engine), on="isbn")
                    .iloc[0]
                   )
    delete_query = f"""DELETE FROM loans
    WHERE friend_id = '{lookup_table["friend_id"]}' AND isbn = '{lookup_table["isbn"]}';"""
    with engine.begin() as connection:
        connection.execute(text(delete_query))
        return f"Removed '{lookup_table["name"]}' borrowed '{lookup_table["title"]}' from 'loans'."
