from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg

DATABASE_URL = "postgresql://postgres:1234@localhost/todo_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)

def notify_channel(session, channel, payload):
    session.execute(text(f"NOTIFY {channel}, '{payload}';"))
    print(f"NOTIFY {channel}, '{payload}'")
    session.commit()