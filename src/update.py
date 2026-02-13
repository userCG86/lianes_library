from sqlalchemy import text
import db

def sanitize_text(new_data):
    if isinstance(new_data, str):
        new_data = new_data.replace("'", "\\'")
    return new_data

def format_field(field):
    if field == "dates":
        return "Contact dates"
    elif field == "isbn":
        return "ISBN"
    else:
        return field.replace("_", " ").capitalize()

def update_friend(friend, field, new_data):
    engine = db.get_engine()
    new_data = sanitize_text(new_data)
    update_query = f"""UPDATE friends 
    SET {field} = '{new_data}' 
    WHERE friend_id = {friend["friend_id"]};"""
    with engine.begin() as connection:
        connection.execute(text(update_query))
        return f"{format_field(field)} updated."

def update_book(book, field, new_data):
    engine = db.get_engine()
    new_data = sanitize_text(new_data)
    update_query = f"""UPDATE books
    SET {field} = '{new_data}'
    WHERE isbn = {book["isbn"]};"""
    with engine.begin() as connection:
        connection.execute(text(update_query))
        return f"{format_field(field)} updated."

def update_loan(loan, field, new_data):
    engine = db.get_engine()
    new_data = sanitize_text(new_data)
    update_query = f"""UPDATE loans
    SET {field} = '{new_data}'
    WHERE isbn = {loan["isbn"]} AND friend_id = {loan["friend_id"]};"""
    if field == 'dates':
        update_query = f"""UPDATE loans
        SET last_contact = '{new_data[0]}', next_contact = '{new_data[1]}'
        WHERE isbn = {loan["isbn"]} AND friend_id = {loan["friend_id"]};"""
    with engine.begin() as connection:
        connection.execute(text(update_query))
        return f"{format_field(field)} updated."
