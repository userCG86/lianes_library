import pandas as pd
import db


def read_friends():
    engine = db.get_engine()
    return pd.read_sql("friends", con=engine)

def display_friends():
    friends = read_friends()
    return friends.drop("friend_id", axis=1).rename({"name": "Name", "max_loans": "Max loans", "notes": "Notes"}, axis=1)

def read_books(available_only=False):
    engine = db.get_engine()
    books = pd.read_sql("books", con=engine)
    if available_only:
        loans = pd.read_sql("loans", con=engine)
        books = pd.merge(books, loans, on="isbn", how="left").query("friend_id.isna()")[books.columns]
    return books

def display_books(available_only=False):
    books = read_books(available_only)
    return books.rename({"title": "Title", "author": "Author", "genre": "Genre", "isbn": "ISBN"}, axis=1)

def read_loans():
    engine = db.get_engine()
    return pd.read_sql("loans", con=engine)

def display_loans():
    friends = read_friends()
    books = read_books()
    loans = read_loans()
    for c in ["loan_date", "last_contact", "next_contact"]:
        loans[c] = loans[c].dt.strftime("%Y-%m-%d")
        
    return pd.merge(loans, friends, on="friend_id", suffixes=["", "_no"]).merge(books, on="isbn")[["title", "name", "loan_date", "last_contact", "next_contact", "notes"]].rename({"title": "Title", "name": "Name", "loan_date": "Loan date", "last_contact": "Last contact", "next_contact": "Next contact", "notes": "Notes"}, axis=1)

if __name__ == "__main__":
    import sys
    from sqlalchemy import create_engine
    sys.path.append("..")
    from con_lib import connection_string
    engine = create_engine(connection_string)
    db.set_engine(engine)

    def final_scorer(score, pass_score):
        print("\n==========")
        if score == pass_score:
            print("Final score: Pass")
        else:
            print(f"Final score: Fail. {score} of {pass_score}.")
        print("==========\n")
    
    val_count = 0
    functions = (
        read_friends(), display_friends(),
        read_books(), display_books(),
        read_loans(), display_loans()
                )
    names = (
        "read_friends", "display_friends",
        "read_books", "display_books",
        "read_loans", "display_loans"
    )
    for f, n in zip(functions, names):
        print(f"{n}: Pass")
        val_count += 1

    final_scorer(val_count, len(functions))