from datetime import datetime
from sqlalchemy import String, and_, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

class Base(DeclarativeBase):
    pass

class UsersRoles(Base):
    __tablename__ = "UsersRoles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(nullable=False, index=True)
    role_id: Mapped[int] = mapped_column(nullable=False)
    created: Mapped[datetime] = mapped_column(insert_default=func.now())

    def find_user_role(session: Session, user_id: int, role_id: int ):
        return session.query(UsersRoles).filter(and_(UsersRoles.user_id == user_id, UsersRoles.role_id == role_id)).first()