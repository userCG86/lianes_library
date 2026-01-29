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