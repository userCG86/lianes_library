import streamlit as st
import pandas as pd
from create import *
from read import *
from validate import *

st.title("Welcome to your Library!")

st.header("Loans")
loan_selection = st.radio("What would you like to do?", options=["Review loans", "Loan a book", ], key="loan_selection")
if loan_selection == "Loan a book":       
    book_df = st.dataframe(display_books(), selection_mode="single-row", on_select="rerun")
    if len(book_df.selection["rows"]) > 0:
        book = read_books().loc[book_df.selection["rows"][0]]

    friend_df = st.dataframe(display_friends(), selection_mode="single-row", on_select="rerun")
    if len(friend_df.selection["rows"]) > 0:
        friend = read_friends().loc[friend_df.selection["rows"][0]]
    try:
        val1 = validate_loan_taker(friend)
        val2 = validate_loan_item(book)
        if val1:
            st.warning(val1)
        if val2:
            st.warning(val2)
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
        
        
        
st.header("Books")
book_selection = st.radio("What would you like to do?", options=["Review books", "Add a book", ], index=None)
if book_selection == "Add a book":
    title = st.text_input("Title:", key="create_title")
    author = st.text_input("Author:", key="create_author")
    genre = st.text_input("Genre:", key="create_genre")
    isbn = st.text_input("ISBN:", key="create_isbn")
    try:
        val1 = validate_title(title)
        val2 = validate_isbn(isbn)
        if val1 and title:
            st.warning(val1)
        if val2 and isbn:
            st.warning(val2)
        if (not val1) & (not val2):
            if st.button("Submit", key="create_book"):
                st.success(create_book(title, author, isbn, genre))
    except NameError:
        pass
    except:
        raise

elif book_selection == "Review books":
    only_available = st.checkbox("Only currently available books", key="only_available")
    st.dataframe(display_books(only_available))


st.header("Friends")
friend_selection = st.radio("What would you like to do?", options=["Review friends", "Add a friend", ], index=None)
if friend_selection == "Review friends":
    st.dataframe(display_friends())

elif friend_selection == "Add a friend":
    friend_name = st.text_input("Name:", key="create_name")
    val = validate_name(friend_name)
    if val and friend_name:
        st.warning(val)
    if not val:
        max_loans = st.number_input("Max loans:", value=2, min_value=1)
        friend_notes = st.text_area("Notes:", key="friend_notes", value=None)
        if st.button("Submit", key="create_friend"):
            st.success(create_friend(friend_name, max_loans, friend_notes))
