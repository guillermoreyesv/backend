from datetime import datetime
from sqlalchemy import Column, String, and_, func
from sqlalchemy.types import JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

class Base(DeclarativeBase):
    pass

class BelvoEndpoints(Base):
    __tablename__ = "BelvoEndpoints"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    type: Mapped[str] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)
    params = Column(JSON)
    code: Mapped[int] = mapped_column(nullable=False)
    full_url: Mapped[str] = mapped_column(nullable=False)
    response = Column(JSON)
    created: Mapped[datetime] = mapped_column(insert_default=func.now())

    def find_endpoint_today(session: Session, type: str, full_url: str, code: int ):
        return session.query(BelvoEndpoints).filter(and_(
            BelvoEndpoints.type == type, 
            BelvoEndpoints.full_url == full_url, 
            BelvoEndpoints.code == code, 
            func.DATE(BelvoEndpoints.created) == datetime.utcnow().date())).first()