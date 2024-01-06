from datetime import datetime
from sqlalchemy import String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(60), nullable=False)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    lastname: Mapped[str] = mapped_column(String(60), nullable=False)
    created: Mapped[datetime] = mapped_column(insert_default=func.now())
    last_connection: Mapped[datetime] = mapped_column(insert_default=func.now())

    def user_exists(session: Session, email: str) -> bool:
        return session.query(User).filter(User.email == email).first()