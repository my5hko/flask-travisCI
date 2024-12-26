from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, MetaData

class Base(DeclarativeBase):
    metadata = MetaData( #creating metadata for db configuration with naming convention to avoid ValueError with sqlite db after db changes
        naming_convention={ #naming convention for db that replaces default naming convention with custom one from dictionary
            "ix": "ix_%(column_0_label)s",  #ix - index, %(column_0_label)s - name of the column
            "uq": "uq_%(table_name)s_%(column_0_name)s", #uq - unique, %(table_name)s - name of the table, %(column_0_name)s - name of the column
            "ck": "ck_%(table_name)s_`%(constraint_name)s`", #ck - check, %(table_name)s - name of the table, %(constraint_name)s - name of the constraint   
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s", #fk - foreign key, %(table_name)s - name of the table, %(column_0_name)s - name of the column, %(referred_table_name)s - name of the referred table   
            "pk": "pk_%(table_name)s", #pk - primary key, %(table_name)s - name of the table
        }
    )

db = SQLAlchemy(model_class=Base)


class Expense(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    amount: Mapped[float]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id")) #creating column for user_id, is foreign key, to create relationship with User table

    user: Mapped["User"] = relationship(back_populates="expenses") #creating relationship with User table

    def __repr__(self):
        return f"Expense(title={self.title}, amount={self.amount})"
    
class User(db.Model): #creating class User inherited from db.Model
    id: Mapped[int] = mapped_column(primary_key=True) #creating column for id, is primary key
    username: Mapped[str] = mapped_column(unique=True) #creating column for username, is unique
    password: Mapped[str] = mapped_column() #creating column for password

    expenses: Mapped[list["Expense"]] = relationship(back_populates="user") #creating relationship with Expense table as list of expenses

    def __init__(self, username, password): #initializing class with username and password

        self.username = username #setting username
        self.password = password #setting password

    def __repr__(self): #returns string representation of the class, is needed for debugging and logging
        return f"User(username={self.username})" #returning string representation of the user