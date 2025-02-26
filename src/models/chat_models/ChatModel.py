import typing

from sqlalchemy import ForeignKey
from sqlalchemy.orm import  Mapped, mapped_column,relationship

from src.db import Base

if typing.TYPE_CHECKING:
    from ..UserModel import User
    from .MessageModel import Message

class Chat(Base):
    __tablename__ = "chat_table"

    id:Mapped[int] = mapped_column(primary_key=True)

    sender_id:Mapped[int] = mapped_column(ForeignKey("user_table.id", ondelete="CASCADE"))
    sender:Mapped["User"] = relationship(uselist=False, foreign_keys=[sender_id])

    recipient_id:Mapped[int] = mapped_column(ForeignKey("user_table.id", ondelete="CASCADE"))
    recipient:Mapped["User"] = relationship(uselist=False, foreign_keys=[recipient_id])

    messages:Mapped[list["Message"]] = relationship(back_populates="chat", uselist=True)
    

