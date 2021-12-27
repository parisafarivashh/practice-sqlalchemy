from sqlalchemy import Column, ForeignKey, \
    Integer, String, create_engine, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine(
    "postgresql+psycopg2://postgres:postgres@localhost/sqlalchemy_practice"
)
Base = declarative_base()


class Member(Base):
    __tablename__ = 'member'

    id = Column(
        Integer,
        primary_key=True,
    )
    title = Column(
        'title',
        String,
        nullable=True,
    )
    first_name = Column(
        'first_name',
        String,
        nullable=False,
    )
    last_name = Column(
        'last_name',
        String,
        nullable=True,
    )
    birthday = Column(
        'birthday',
        Date,
        nullable=True,
    )
    rooms = relationship(
        'Room',
        back_populates='member',
        lazy='joined',
    )
    messages = relationship(
        'Message',
        back_populates='member',
        lazy='joined',
    )


class Room(Base):
    __tablename__ = 'room'

    id = Column(
        Integer,
        primary_key=True,
    )
    title = Column(
        'title',
        String,
        nullable=False,
    )
    creator_id = Column(
        'creator_id',
        Integer,
        ForeignKey('member.id'),
    )
    creator = relationship(
        'Member',
        order_by='room.id',
        back_populates='rooms',
        lazy='joined',
    )
    messages = relationship(
        'Message',
        order_by='room.id',
        back_populates='room',
        lazy='joined',
    )


class Message(Base):
    __tablename__ = 'message'

    id = Column(
        Integer,
        primary_key=True,
    )
    sender_id = Column(
        Integer,
        ForeignKey('member.id'),
    )
    sender = relationship(
        'Member',
        back_populates='messages',
        lazy='joined',
    )
    body = Column(
        'body',
        String,
        nullable=True,
    )
    room_id = Column(
        Integer,
        ForeignKey('room.id'),
    )
    room = relationship(
        'Room',
        back_populates='message',
        lazy='joined',
    )


Base.metadata.create_all(bind=engine)

