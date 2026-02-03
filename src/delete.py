import pandas as pd
from sqlalchemy import create_engine, text

import sys
sys.path.append("..")
from con_lib import connection_string

engine = create_engine(connection_string)

def delete_friend(friend):
    delete_query = f"""DELETE FROM friends
    WHERE friend_id = '{friend["friend_id"]}';"""
    with engine.begin() as connection:
        connection.execute(text(delete_query))
        return f"Removed '{friend['name']}' from 'friends'."

def delete_book(book):
    delete_query = f"""DELETE FROM books
    WHERE isbn = '{book["isbn"]}';"""
    with engine.begin() as connection:
        connection.execute(text(delete_query))
        return f"Removed '{book['title']}' from 'books'."

def delete_loan(loan):
    lookup_table = (pd.read_sql("loans", con=connection_string).loc[[loan.name]]
                    .merge(pd.read_sql("friends", con=connection_string), on="friend_id")
                    .merge(pd.read_sql("books", con=connection_string), on="isbn")
                    .iloc[0]
                   )
    delete_query = f"""DELETE FROM loans
    WHERE friend_id = '{lookup_table["friend_id"]}' AND isbn = '{lookup_table["isbn"]}';"""
    with engine.begin() as connection:
        connection.execute(text(delete_query))
        return f"Removed '{lookup_table["name"]}' borrowed '{lookup_table["title"]}' from 'loans'."

if __name__ == "__main__":
    def final_scorer(score, pass_score):
        print()
        if score == pass_score:
            print("Final score: Pass")
        else:
            print(f"Final score: Fail. {score} of {pass_score}.")
        print("==========\n")
    def validation_loop(input_, table, f):
        indentifiers = {"friends": "name", "books": "title", "loans": ["friend_id", "isbn"]}
        outputs = []
        for in_ in input_:
            table_pre = pd.read_sql(table, con=connection_string)
            f(in_)
            table_post = pd.read_sql(table, con=connection_string)

            dropped_line = pd.concat([table_pre, table_post]).drop_duplicates(keep=False).iloc[0]
            outputs.append(dropped_line)
        val_score = 0
        for i, o in zip(input_, outputs):
            if i.equals(o):
                print("Pass.")
                val_score += 1
            else:
                print(f"Failed. {[identifiers[table]]}: {i[identifiers[table]]}")
        
        final_scorer(val_score, len(input_))


    print("\nDelete friend\n==========")
    friend = pd.read_sql("friends", con=connection_string).sample().iloc[0]
    validation_loop((friend,), "friends", delete_friend)

    print("\nDelete book\n==========")
    book = pd.read_sql("books", con=connection_string).sample().iloc[0]
    validation_loop((book,), "books", delete_book)
    
    print("\nDelete loan\n==========")
    loan = pd.read_sql("loans", con=connection_string).sample().iloc[0]
    validation_loop((loan,), "loans", delete_loan)
