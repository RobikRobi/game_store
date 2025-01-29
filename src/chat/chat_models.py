import typing

from sqlalchemy import ForeignKey
from sqlalchemy.orm import  Mapped, mapped_column,relationship

from src.db import Base

if typing.TYPE_CHECKING:
    from src.app_auth.auth_models import User

class Chat(Base):
    __tablename__ = "chat_tabel"

    id:Mapped[int] = mapped_column(primary_key=True)

    user_one_id:Mapped[int] = mapped_column(ForeignKey("user_tabel.id", ondelete="CASCADE"))
    user_one:Mapped["User"] = relationship(uselist=False, foreign_keys=[user_one_id])

    user_two_id:Mapped[int] = mapped_column(ForeignKey("user_tabel.id", ondelete="CASCADE"))
    user_two:Mapped["User"] = relationship(uselist=False, foreign_keys=[user_two_id])

    messages:Mapped[list["Message"]] = relationship(back_populates="chat", uselist=True)
    

class Message(Base):
    __tablename__ = "message_table"

    id:Mapped[int] = mapped_column(primary_key=True)

    text:Mapped[str]

    chat_id:Mapped[int] = mapped_column(ForeignKey("chat_table.id", ondelete="CASCADE"))
    chat:Mapped["Chat"] = relationship(back_populates="messages", uselist=False)