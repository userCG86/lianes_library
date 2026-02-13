import pandas as pd
import db



def validate_name(name):
    if (name is None) or (not name.strip()):
        return "Warning. Empty name not accepted."
    else:
        return ""

def validate_isbn(isbn):
    engine = db.get_engine()
    if len(isbn) not in (10, 13):
        return "Warning. ISBN must be 10 or 13 digits long."
    elif not isbn.isnumeric():
        return "Warning. ISBN must be numeric."
    elif isbn in pd.read_sql("SELECT isbn FROM books", con=engine)["isbn"].values:
        return "Warning. This ISBN is already in use."
    else:
        return ""

def validate_title(title):
    if (title is None) or (not title.strip()):
        return "Warning. Empty title not accepted."
    else:
        return ""

def validate_loan_taker(friend):
    engine = db.get_engine()
    current_loans = pd.read_sql("loans", con=engine)
    if friend["friend_id"] in current_loans["friend_id"].unique():
        num_loans = current_loans.value_counts("friend_id").loc[friend["friend_id"]]
        if friend["max_loans"] == num_loans:
            return f"Warning. {friend["name"]} has already reached their maximum loan allowance."
    else:
        return ""

def validate_loan_item(book):
    engine = db.get_engine()
    current_loans = pd.read_sql("loans", con=engine)
    if book["isbn"] in current_loans["isbn"].values:
        return f"Warning. {book["title"]} is already on loan."
    else:
        return ""
