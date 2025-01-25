from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import date

class Odpoved(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    fname: str
    lname: str
    email: str
    phone: str
    message: str
    date: date 

