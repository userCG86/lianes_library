# from sqlalchemy import create_engine

engine = None

def set_engine(e):
    global engine
    engine = e

def get_engine():
    return engine