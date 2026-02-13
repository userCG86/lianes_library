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


if __name__ == "__main__":
    from functools import partial
    
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
    def validation_loop(input_, expected_):
        outputs = []
        for in_ in input_:
            out = in_()
            outputs.append((in_.func.__name__, out))
        val_score = 0
        for i, o in zip(expected_, outputs):
            if i[0] == list(o[1].columns):
                if i[1] == o[1].shape[0]:
                    print(f"{o[0]}: Pass")
                    val_score += 1
                elif o[1].empty:
                    print(f"Failed. {o[0]}: No data")
                else:
                    print(f"Failed. {o[0]}: Expected {i[1]} lines, read {o[1].shape[0]}")
            else:
                print(f"Failed. {o[0]}: columns {list(o[1].columns)}")

        final_scorer(val_score, len(input_))
        
    
    print("\nRead friends\n==========")
    reads = (
        partial(read_friends), 
        partial(display_friends)
    )
    expected = (
        (['friend_id', 'name', 'max_loans', 'notes'], 6), 
        (['Name', 'Max loans', 'Notes'], 6)
    )
    validation_loop(reads, expected)

    print("\nRead books\n==========")
    reads = (
        partial(read_books), 
        partial(read_books, True), 
        partial(display_books),
        partial(display_books, True)
    )
    expected = (
        (['title', 'author', 'genre', 'isbn'], 10), 
        (['title', 'author', 'genre', 'isbn'], 6), 
        (['Title', 'Author', 'Genre', 'ISBN'], 10),
        (['Title', 'Author', 'Genre', 'ISBN'], 6)
    )
    validation_loop(reads, expected)

    print("\nRead loans\n==========")
    reads = (
        partial(read_loans), 
        partial(display_loans)
    )
    expected = (
        (['isbn', 'friend_id', 'loan_date', 'last_contact', 'next_contact', 'notes'], 4), 
        (['Title', 'Name', 'Loan date', 'Last contact', 'Next contact', 'Notes'], 4)
    )
    validation_loop(reads, expected)