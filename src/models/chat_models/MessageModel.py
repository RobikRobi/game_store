import typing

from sqlalchemy import ForeignKey
from sqlalchemy.orm import  Mapped, mapped_column,relationship

from src.db import Base

if typing.TYPE_CHECKING:
    from .ChatModel import Chat

class Message(Base):
    __tablename__ = "message_table"

    id:Mapped[int] = mapped_column(primary_key=True)

    text:Mapped[str]

    chat_id:Mapped[int] = mapped_column(ForeignKey("chat_table.id", ondelete="CASCADE"))
    chat:Mapped["Chat"] = relationship(back_populates="messages", uselist=False)