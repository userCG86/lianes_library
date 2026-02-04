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

if __name__ == "__main__":
    from functools import partial

    import sys
    from sqlalchemy import create_engine
    sys.path.append("..")
    from con_lib import connection_string
    engine = create_engine(connection_string)
    db.set_engine(engine)
    
    def final_scorer(score, pass_score):
        print()
        if score == pass_score:
            print("Final score: Pass")
        else:
            print(f"Final score: Fail. {score} of {pass_score}.")
        print("==========\n")
    def validation_loop(input_, expected_, type_, table):
        outputs = []
        for in_ in input_:
            table_pre = pd.read_sql(table, con=engine)
            in_()
            table_post = pd.read_sql(table, con=engine)

            new_line = (pd.concat([table_pre, table_post])
                        .drop_duplicates(keep=False)
                        .iloc[0]
                        .fillna("N/A")
                       )
            outputs.append(new_line)
        val_score = 0
        for i, o in zip(expected_, outputs):
            for j in i:
                if j in o.values:
                    continue
                else:
                    print(f"Failed. {type_}: {i} not sent to table.")
                    break
            else:
                print("Pass.")
                val_score += 1
                    
        final_scorer(val_score, len(input_))
            
    print("\nCreate friend\n==========")
    friends = (partial(create_friend, "Edd"),
               partial(create_friend, "Eddy", 1),
               partial(create_friend, "Ed", notes="Not sure he can read"))
    expected = (("Edd", 2, "N/A"), 
                ("Eddy", 1, "N/A"), 
                ("Ed", 2, "Not sure he can read")
               )
    validation_loop(friends, expected, "Name", "friends")

    print("\nCreate book\n==========")
    books = (partial(create_book, "Words on a Page", "0000000000000"),
             partial(create_book, "Alice's Big Nap".replace("'", "\'"), "0000000000001", author="A. Snooze"),
             partial(create_book, "Holy Words on a Page", "0000000000002", genre="Religion")
            )
    expected = (("Words on a Page", "0000000000000", "N/A", "N/A"), 
                ("Alice's Big Nap", "0000000000001", "A. Snooze", "N/A"), 
                ("Holy Words on a Page", "0000000000002", "N/A", "Religion")
               )
    validation_loop(books, expected, "Title", "books")

    print("\nCreate loan\n==========")
    loans = (partial(create_loan, pd.read_sql("SELECT * FROM friends WHERE friend_id = 6", con=engine).iloc[0], pd.read_sql("SELECT * FROM books WHERE ISBN = '9785566778899'", con=engine).iloc[0]),
             partial(create_loan, pd.read_sql("SELECT * FROM friends WHERE friend_id = 1", con=engine).iloc[0], pd.read_sql("SELECT * FROM books WHERE ISBN = '9780062316110'", con=engine).iloc[0], '2026-01-01'),
             partial(create_loan, pd.read_sql("SELECT * FROM friends WHERE friend_id = 2", con=engine).iloc[0], pd.read_sql("SELECT * FROM books WHERE ISBN = '9780385490818'", con=engine).iloc[0], next_contact='2026-02-15'),
             partial(create_loan, pd.read_sql("SELECT * FROM friends WHERE friend_id = 5", con=engine).iloc[0], pd.read_sql("SELECT * FROM books WHERE ISBN = '9780143127741'", con=engine).iloc[0], notes="Test note."),
            )
    today = pd.Timestamp.today().date()
    expected = (("9785566778899", 6,  pd.Timestamp(today), "N/A", pd.Timestamp(today+pd.Timedelta(30, "d")), "N/A"),
                ("9780062316110", 1, pd.Timestamp('2026-01-01'), "N/A", pd.Timestamp(today+pd.Timedelta(30, "d")), "N/A"),
                ("9780385490818", 2, pd.Timestamp(today), "N/A", pd.Timestamp('2026-02-15'), "N/A"),
                ("9780143127741", 5,  pd.Timestamp(today), "N/A", pd.Timestamp(today+pd.Timedelta(30, "d")), "Test note.")
               )
    validation_loop(loans, expected, "Title", "loans")
