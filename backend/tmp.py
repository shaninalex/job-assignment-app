from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from sqlalchemy.exc import DatabaseError, IntegrityError

from sqlalchemy import create_engine


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str] = mapped_column(String(30), unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")


if __name__ == "__main__":
    engine = create_engine("sqlite:///sales.db", echo=False)
    Base.metadata.create_all(engine)
    cc_cookie = User(
        name="buddy",
        fullname="Buddy Harsdf",
        addresses=[
            Address(email_address="test@test.com"),
            Address(email_address="test2@test.com"),
        ],
    )
    with Session(engine) as session:
        try:
            session.add(cc_cookie)
            session.commit()
            session.close()

        except DatabaseError as e:

            print("\nError:", e)
            print(e.detail)
            print(e.args)
            print(e.code)
            print(type(e))
            if type(e) is IntegrityError:
                print("Duplicates not allowed")
            print("\n")
            session.rollback()
            session.close()

    with Session(engine) as session:
        smt = select(Address)
        for addr in session.scalars(smt):
            print(addr.user)

        for user in session.scalars(select(User)):
            print("user addresses: \n", user.addresses)
