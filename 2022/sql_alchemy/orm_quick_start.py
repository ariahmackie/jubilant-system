#source: https://docs.sqlalchemy.org/en/14/orm/quickstart.html
# Notes
# Object relational mapping makes relationships between objects and groups of values in a database possible.
# This allows persistant objects. Previously I was trying to write the relationships myself but sqlalchemy is designed for this.
#SQL alchemy uses a data mapper pattern instead of active record as its ORM
#

# Models
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

#Engine
from sqlalchemy import create_engine

#####################################
# How to declare Models
#
####################################
Base = declarative_base()

class User(Base):
    __tablename__ = "user_account"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String)

    addresses = relationship("Address", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)

    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"

##############################
# how to create an engine
engine = create_engine("sqlite://", echo=True, future=True)
####################################
