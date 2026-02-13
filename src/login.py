import streamlit as st
from sqlalchemy import create_engine, exc

import db

def login():
    schema = "sample_library"
    host = "127.0.0.1"
    port = 3306
    user = st.text_input("Username", key="username")
    password = st.text_input("Password", key="password", type="password")
    connection_string = f'mysql+pymysql://{user}:{password}@{host}:{port}/{schema}'
    if (not user == "") & (not password == ""):
        try:
            engine = create_engine(connection_string)
            engine.connect()
            db.set_engine(engine)
            st.session_state["engine"] = engine
            st.session_state["login"] = "loggedin"
            st.rerun()
        except exc.OperationalError:
            st.warning("username incorrect")
        except RuntimeError:
            st.warning("password incorrect")
            