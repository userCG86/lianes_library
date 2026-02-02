import pandas as pd

import sys
sys.path.append("..")
from con_lib import connection_string

def validate_name(name):
    if not name:
        return "Warning. Empty name not accepted."
    else:
        return ""

def validate_isbn(isbn):
    if len(isbn) not in (10, 13):
        return "Warning. ISBN must be 10 or 13 digits long."
    elif not isbn.isnumeric():
        return "Warning. ISBN must be numeric."
    elif isbn in pd.read_sql("SELECT isbn FROM books", con=connection_string)["isbn"].values:
        return "Warning. This ISBN is already in use."
    else:
        return ""

def validate_title(title):
    if not title:
        return "Warning. Empty title not accepted."
    else:
        return ""

def validate_loan_taker(friend):
    current_loans = pd.read_sql("loans", con=connection_string)
    if friend["friend_id"] in current_loans["friend_id"].unique():
        if friend["max_loans"] == current_loans.value_counts("friend_id").loc[friend["friend_id"]]:
            return f"Warning. {friend["name"]} has already reached their maximum loan allowance."
    else:
        return ""

def validate_loan_item(book):
    current_loans = pd.read_sql("loans", con=connection_string)
    if book["isbn"] in current_loans["isbn"].values:
        return f"Warning. {book["title"]} is already on loan."
    else:
        return ""

if __name__ == "__main__":
    def final_scorer(score, pass_score):
        print()
        if score == pass_score:
            print("Final score: Pass")
        else:
            print(f"Final score: Fail. {score} of {pass_score}.")
        print("==========\n")

    def validation_loop(input_, expected_, type_, f):
        outputs = []
        for in_ in input_:
            outputs.append(f(in_))
        val_score = 0
        for i, o in zip(expected_, outputs):
            if i == o:
                print("Pass.")
                val_score += 1
            else:
                print(f"Failed. {type_}: {i}. Output: {o}")
        final_scorer(val_score, len(input_))

    print("\nValidate name\n==========")
    names = ("Edd", "", None)
    expected = ("", "Warning. Empty name not accepted.", "Warning. Empty name not accepted.")
    validation_loop(names, expected, "Name", validate_name)

    print("\nValidate ISBN\n==========")
    isbns = ("0000000000000", "00001", "000000000a", "9780987654321")
    expected = ("", "Warning. ISBN must be 10 or 13 digits long.", "Warning. ISBN must be numeric.", "Warning. This ISBN is already in use.")
    validation_loop(isbns, expected, "ISBN", validate_isbn)

    print("\nValidate title\n==========")
    titles = ("Words on a Page", "", None)
    expected = ("", "Warning. Empty title not accepted.", "Warning. Empty title not accepted.")
    validation_loop(titles, expected, "Title", validate_title)

    print("\nValidate borrower\n==========")
    borrowers = (pd.read_sql("SELECT * FROM friends WHERE friend_id = 6", con=connection_string).iloc[0], # Soso Klein
                 pd.read_sql("SELECT * FROM friends WHERE friend_id = 3", con=connection_string).iloc[0] # Luca Schmidt
                )
    expected = ("", f"Warning. {borrowers[1]["name"]} has already reached their maximum loan allowance.")
    validation_loop(borrowers, expected, "Borrower", validate_loan_taker)

    print("\nValidate loan item\n==========")
    items = (pd.read_sql("SELECT * FROM books WHERE ISBN = '9785566778899'", con=connection_string).iloc[0], # Gardens of Glass
             pd.read_sql("SELECT * FROM books WHERE ISBN = '9781122334455'", con=connection_string).iloc[0] # The Secret Ingredient
            )
    expected = ("", f"Warning. {items[1]["title"]} is already on loan.")
    validation_loop(items, expected, "Title", validate_loan_item)