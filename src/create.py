import pandas as pd
from sqlalchemy import create_engine, text

import sys
sys.path.append("..")
from con_lib import connection_string
from validate import *

def create_friend(name, max_loans=2, notes=None):
    df = pd.DataFrame(
        [[name, max_loans]],
        columns=["name", "max_loans"]
    )
    df.to_sql(
        "friends", 
        if_exists="append", 
        con=connection_string, 
        index=False
    )
    message = f"Added '{name}' to 'friends'."
    
    return message

def create_book(title, author, isbn, genre=None):
    df = pd.DataFrame(
        [[title, author, genre, isbn]], 
        columns=["title", "author", "genre", "isbn"]
    )
    df.to_sql(
        "books",
        if_exists="append", 
        con=connection_string, 
        index=False
    )
    message = f"Added '{title}' to 'books'."
        
    return message

def create_loan(friend, book, loan_date=pd.Timestamp.today().date(), next_contact=pd.Timestamp.today().date() + pd.Timedelta(30, "d"), notes=None):
    df = pd.DataFrame(
        [[book["isbn"], friend["friend_id"], loan_date, next_contact, notes]],
        columns = ["isbn", "friend_id", "loan_date", "next_contact", "notes"]
    )
    df.to_sql(
        "loans",
        if_exists="append",
        con=connection_string,
        index=False
    )
    message = f"Added '{friend["name"]}' borrowed '{book["title"]}' to 'loans'."

    return message

if __name__ == "__main__":
    def final_scorer(score, pass_score):
        print("\n==========")
        if score == pass_score:
            print("Final score: Pass")
        else:
            print(f"Final score: Fail. {score} of {pass_score}.")
        print("==========\n")
            
    engine = create_engine(connection_string)

    friends = ("Edd", "")
    val_count = 0

    for friend in friends:
        val = validate_name(friend)
        if not val:
            if create_friend(friend) == f"Added '{friend}' to 'friends'.":
                print("Create friend: Pass")
                val_count += 1
                id = pd.read_sql("SELECT MAX(friend_id) FROM friends", con=connection_string).iloc[0,0]
                with engine.begin() as connection:
                    connection.execute(text(f"DELETE FROM friends WHERE friend_id = {id}"))
            else: 
                print(f"Create friend: Fail. Friend: '{friend}'")
        elif val == "Warning. Empty name not accepted.":
            print("Validate empty name: Pass")
            val_count += 1
        else:
            print(f"Validate friend: Fail. Friend: '{friend}'")
    
    final_scorer(val_count, len(friends))

    books = (
        ("Words on a Page", "A. Snooze", "0000000000000", "boring"),
        ("Alice's Big Nap", "A. Snooze", "00001", "boring"),
        ("Alice's Big Nap", "A. Snooze", "000000000a", "boring"),
        ("Alice's Big Nap", "A. Snooze", "9780987654321", "boring"),
        ("", "A. Snooze", "0000000000", "boring")
    )
    val_count = 0
    
    for book in books:
        val1 = validate_isbn(book[2])
        val2 = validate_title(book[0])
        if (not val1) & (not val2):
            if create_book(*book) == f"Added '{book[0]}' to 'books'.":
                print("Create book: Pass")
                val_count += 1
                with engine.begin() as connection:
                    connection.execute(text(f"DELETE FROM books WHERE isbn = {book[2]}"))
            else:
                print(f"Create book: Fail. Title: '{book[0]}'")
        elif val1:
            if val1 == "Warning. ISBN must be 10 or 13 digits long.":
                print("Validate ISBN wrong length: Pass")
                val_count += 1
            elif val1 == "Warning. ISBN must be numeric.":
                print("Validate ISBN numeric: Pass")
                val_count += 1
            elif val1 == "Warning. This ISBN is already in use.":
                print("Validate ISBN unique: Pass")
                val_count += 1
            else:
                print(f"Validate ISBN: Failed. ISBN: '{book[2]}'")
        elif val2 == "Warning. Empty title not accepted.":
            print("Validate empty title: Pass")
            val_count += 1
        else:
            print(f"Validate book: Failed. Title: '{book[0]}', ISBN: '{book[2]}'")
    
    final_scorer(val_count, len(books))
    
    loans = (
        (pd.read_sql("SELECT * FROM friends WHERE friend_id = 6", con=connection_string).iloc[0], # Soso Klein
         pd.read_sql("SELECT * FROM books WHERE ISBN = '9785566778899'", con=connection_string).iloc[0]), # Gardens of Glass
        (pd.read_sql("SELECT * FROM friends WHERE friend_id = 3", con=connection_string).iloc[0], # Luca Schmidt
         pd.read_sql("SELECT * FROM books WHERE ISBN = '9785566778899'", con=connection_string).iloc[0]), # Gardens of Glass
        (pd.read_sql("SELECT * FROM friends WHERE friend_id = 6", con=connection_string).iloc[0], # Soso Klein
         pd.read_sql("SELECT * FROM books WHERE ISBN = '9781122334455'", con=connection_string).iloc[0]) # The Secret Ingredient
    )
    val_count = 0
    
    for loan in loans:
        val1 = validate_loan_taker(loan[0])
        val2 = validate_loan_item(loan[1])
        if (not val1) & (not val2):
            if create_loan(*loan) == f"Added '{loan[0]["name"]}' borrowed '{loan[1]["title"]}' to 'loans'.":
                print("Create loan: Pass")
                val_count += 1
                with engine.begin() as connection:
                    connection.execute(text(f"DELETE FROM loans WHERE isbn = {loan[1]["isbn"]} AND friend_id = {loan[0]["friend_id"]}"))
            else:
                print(f"Create loan: Failed. Friend: '{loan[0]["name"]}', Title: '{loan[1]["title"]}'")
        elif val1 == f"Warning. {loan[0]["name"]} has already reached their maximum loan allowance.":
            print("Validate friend max loans: Pass")
            val_count += 1
        elif val2 == f"Warning. {loan[1]["title"]} is already on loan.":
            print("Validate already on loan: Pass")
            val_count += 1
        else:
            print(f"Validate loan: Failed. Friend: '{loan[0]["name"]}', Title: '{loan[1]["title"]}'")
    
    final_scorer(val_count, len(loans))