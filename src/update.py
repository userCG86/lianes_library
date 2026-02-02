from sqlalchemy import create_engine, text

import sys
sys.path.append("..")
from con_lib import connection_string

engine = create_engine(connection_string)

def update_friend(friend, field, new_data):
    update_query = f"""UPDATE friends 
    SET {field} = '{new_data}' 
    WHERE friend_id = {friend["friend_id"]};"""
    with engine.begin() as connection:
        connection.execute(text(update_query))
        return "Update successful."

def update_book(book, field, new_data):
    update_query = f"""UPDATE books
    SET {field} = '{new_data}'
    WHERE isbn = {book["isbn"]};"""
    with engine.begin() as connection:
        connection.execute(text(update_query))
        return "Update successful."

def update_loan(loan, field, new_data):
    update_query = f"""UPDATE loans
    SET {field} = '{new_data}'
    WHERE isbn = {loan["isbn"]} AND friend_id = {loan["friend_id"]};"""
    if field == 'dates':
        update_query = f"""UPDATE loans
        SET last_contact = '{new_data[0]}', next_contact = '{new_data[1]}'
        WHERE isbn = {loan["isbn"]} AND friend_id = {loan["friend_id"]};"""
    with engine.begin() as connection:
        connection.execute(text(update_query))
        return "Update successful."


if __name__ == "__main__":
    import pandas as pd
    
    def final_scorer(score, pass_score):
        print()
        if score == pass_score:
            print("Final score: Pass")
        else:
            print(f"Final score: Fail. {score} of {pass_score}.")
        print("==========\n")
    def validation_loop(input_, expected_, type_, table, f):
        primaries = {"friends": ["friend_id"], "books": ["isbn"], "loans": ["friend_id", "isbn"]}
        outputs = []
        for in_ in input_:
            f(*in_)
            if in_[1] == 'dates':
                to_read = "last_contact, next_contact"
            else:
                to_read = in_[1]
            outputs.append(pd.read_sql(f"SELECT {to_read} FROM {table} WHERE {" AND ".join([f"{id} = {in_[0][id]}" for id in primaries[table]])};", con=connection_string).iloc[0].to_list())
        val_score = 0
        for i, o, t in zip(expected_, outputs, type_):
            if i == o:
                print("Pass.")
                val_score += 1
            else: 
                print(f"Failed. '{i}'({t}) not sent to table.", o)
                    
        final_scorer(val_score, len(input_))
    
    # engine = create_engine(connection_string)

    print("\nUpdate friend\n==========")
    friend = pd.read_sql("SELECT * FROM friends WHERE friend_id = 6", con=connection_string).iloc[0]
    updates = (
        (friend, 'name', 'Soso'),
        (friend, 'max_loans', 2),
        (friend, 'notes', "Doesn't answer phone, use socials.".replace("'", "\\'")) #replace not needed in streamlit
    )
    expected = (["Soso"], [2], ["Doesn't answer phone, use socials."])
    validation_loop(updates, expected, [u[1] for u in updates], "friends", update_friend)

    print("\nUpdate book\n==========")
    book = pd.read_sql("SELECT * FROM books WHERE isbn = '9785566778899'", con=connection_string).iloc[0]
    updates = (
        (book, 'title', 'A Study in Boredom'),
        (book, 'author', 'A. Snooze'),
        (book, 'genre', 'Boring')
    )
    expected = (['A Study in Boredom'], ['A. Snooze'], ['Boring'])
    validation_loop(updates, expected, [u[1] for u in updates], "books", update_book)

    print("\nUpdate loan\n==========")
    loan = pd.read_sql("SELECT * FROM loans WHERE isbn = '9780987654321' AND friend_id = 5", con=connection_string).iloc[0]
    today = pd.Timestamp.today().date()
    next_week = today + pd.Timedelta(1, "w")
    updates = (
        (loan, 'notes', "Got caught in rainstorm with book"),
        (loan, 'dates', (today,  next_week))
    )
    expected = (["Got caught in rainstorm with book"], [today, next_week])
    validation_loop(updates, expected, [u[1] for u in updates], "loans", update_loan)
    
        