import streamlit as st
import pandas as pd
from create import *
from read import *
from validate import *
from update import *
from delete import *

st.title("Welcome to your Library!")

st.header("Loans")
loan_selection = st.radio("What would you like to do?", options=["Review loans", "Loan a book", "Update a loan", "Return a book"], key="loan_selection")
if loan_selection == "Loan a book":       
    book_df = st.dataframe(display_books(), selection_mode="single-row", on_select="rerun")
    if len(book_df.selection["rows"]) > 0:
        book = read_books().loc[book_df.selection["rows"][0]]
        val1 = validate_loan_item(book)
        if val1:
            st.warning(val1)
    friend_df = st.dataframe(display_friends(), selection_mode="single-row", on_select="rerun")
    if len(friend_df.selection["rows"]) > 0:
        friend = read_friends().loc[friend_df.selection["rows"][0]]
        val2 = validate_loan_taker(friend)
        if val2:
            st.warning(val2)
    try:
        if (not val1) & (not val2):
            loan_date = st.date_input("Loan date", key="loan_date")
            next_contact = st.date_input("Next check date", value=pd.Timestamp.today().date() + pd.Timedelta(30, "d"), key="loan_next_contact")
            loan_notes = st.text_area("Notes", key="loan_notes", value=None)
            if st.button("Submit", key="create_loan"):
                st.success(create_loan(friend, book, loan_date, next_contact, loan_notes))
    except NameError:
        pass
    except:
        raise

elif loan_selection == "Review loans":
    st.dataframe(display_loans())

elif loan_selection == "Update a loan":
    loan_df = st.dataframe(display_loans(), selection_mode="single-row", on_select="rerun")
    if len(loan_df.selection["rows"]) > 0:
        loan = read_loans().loc[loan_df.selection["rows"][0]]
        loan_part = st.selectbox("What would you like to update?", ["Contact dates", "Notes"], key="loan_part", index=None)
        if loan_part == "Contact dates":
            last_contact = st.date_input("Last contact date", key="last_date")
            next_contact = st.date_input("Last contact date", key="next_date", value=pd.Timestamp.today().date() + pd.Timedelta(14, "d"))
            if st.button("Submit", key="submit_loan_dates"):
                st.success(update_loan(loan, "dates", [last_contact, next_contact]))
        elif loan_part == "Notes":
            notes = st.text_area("", key="update_loan_notes", value=loan["notes"])
            if st.button("Submit", key="submit_loan_notes"):
                st.success(update_loan(loan, "notes", notes))

elif loan_selection == "Return a book":
    loan_df = st.dataframe(display_loans(), selection_mode="single-row", on_select="rerun")
    if len(loan_df.selection["rows"]) > 0:
        loan = read_loans().loc[loan_df.selection["rows"][0]]
        if st.button("Confirm", key="delete_loan"):
            st.success(delete_loan(loan))
        
        
st.header("Books")
book_selection = st.radio("What would you like to do?", options=["Review books", "Add a book", "Update a book", "Remove a book"], index=None)
if book_selection == "Add a book":
    title = st.text_input("Title:", key="create_title")
    if title:
        val1 = validate_title(title)
        if val1:
            st.warning(val1)
    author = st.text_input("Author:", key="create_author")
    genre = st.text_input("Genre:", key="create_genre")
    isbn = st.text_input("ISBN:", key="create_isbn")
    if isbn:
        val2 = validate_isbn(isbn)
        if val2:
            st.warning(val2)
    try:
        if (not val1) & (not val2):
            if st.button("Submit", key="create_book"):
                st.success(create_book(title, isbn, author, genre))
    except NameError:
        pass
    except:
        raise

elif book_selection == "Review books":
    only_available = st.checkbox("Only currently available books", key="only_available")
    st.dataframe(display_books(only_available))

elif book_selection == "Update a book":
    book_df = st.dataframe(display_books(), selection_mode="single-row", on_select="rerun")
    if len(book_df.selection["rows"]) > 0:
        book = read_books().loc[book_df.selection["rows"][0]]
        book_part = st.selectbox("What would you like to update?", ["Title", "Author", "Genre", "ISBN"], key="book_part", index=None)
        if book_part:
            to_update_book = st.text_input("", key="update_book_entry")
        try:
            if book_part == "ISBN" and to_update_book:
                val = validate_isbn(to_update_book)
            elif book_part == "Title" and to_update_book:
                val = validate_title(to_update_book)
            elif book_part in ("Author", "Genre"):
                val = ""
            if val:
                st.warning(val)
            else:
                if st.button("Submit", key="submit_book_update"):
                    field = book_part.lower()
                    st.success(update_book(book, field, to_update_book))
        except NameError:
            pass
        except:
            raise

elif book_selection == "Remove a book":
    book_df = st.dataframe(display_books(), selection_mode="single-row", on_select="rerun")
    if len(book_df.selection["rows"]) > 0:
        book = read_books().loc[book_df.selection["rows"][0]]
        if st.button("Confirm", key="delete_book"):
            st.success(delete_book(book))


st.header("Friends")
friend_selection = st.radio("What would you like to do?", options=["Review friends", "Add a friend", "Update a friend", "Remove a friend"], index=None)
if friend_selection == "Review friends":
    st.dataframe(display_friends())

elif friend_selection == "Add a friend":
    friend_name = st.text_input("Name:", key="create_name")
    val = validate_name(friend_name)
    if val and friend_name:
        st.warning(val)
    if not val:
        max_loans = st.number_input("Max loans:", value=2, min_value=1, key="create_max_loans")
        friend_notes = st.text_area("Notes:", key="create_friend_notes", value=None)
        if st.button("Submit", key="create_friend"):
            st.success(create_friend(friend_name, max_loans, friend_notes))

elif friend_selection == "Update a friend":
    friend_df = st.dataframe(display_friends(), selection_mode="single-row", on_select="rerun")
    if len(friend_df.selection["rows"]) > 0:
        friend = read_friends().loc[friend_df.selection["rows"][0]]
        friend_part = st.selectbox("What would you like to update?", ["Name", "Max loans", "Notes"], key="friend_part", index=None)
        if friend_part == "Name":
            to_update_friend = st.text_input("", key="update_name")
            val = validate_name(to_update_friend)
            if val and to_update_friend:
                st.warning(val)
        elif friend_part == "Max loans":
            to_update_friend = st.number_input("", value=friend["max_loans"], min_value=1, key="update_max_loans")
            val = ""
        elif friend_part == "Notes":
            to_update_friend = st.text_area("", key="update_friend_notes", value=friend["notes"])
            val = ""
        try:
            if not val:
                if st.button("Submit", key="update_friend"):
                    field = friend_part.lower().replace(" ", "_")
                    st.success(update_friend(friend, field, to_update_friend))
        except NameError:
            pass
        except:
            raise

elif friend_selection == "Remove a friend":
    friend_df = st.dataframe(display_friends(), selection_mode="single-row", on_select="rerun")
    if len(friend_df.selection["rows"]) > 0:
        friend = read_friends().loc[friend_df.selection["rows"][0]]
        if st.button("Confirm", key="delete_friend"):
            st.success(delete_friend(friend))