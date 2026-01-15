# SQLite engine (file-based). For tests/dev use, file is `database.db` in workspace.
from sqlalchemy import create_engine
from sqlmodel import SQLModel


DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL, echo=False)



