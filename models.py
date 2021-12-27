import pytest

from sqlalchemy import Column, ForeignKey, \
    Integer, String, create_engine, Date
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine(
    'postgresql+psycopg2://postgres:postgres@localhost/sqlalchemy_practice'
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
    creator_room = relationship(
        'Room',
        back_populates='creator',
        lazy='joined',
    )
    messages = relationship(
        'Message',
        back_populates='sender',
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
        back_populates='creator_room',
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
        back_populates='messages',
        lazy='joined',
    )


Base.metadata.create_all(bind=engine)


class Test:

    @pytest.fixture
    def setup(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()

        self.member_1 = Member(
            title='first_title',
            first_name='parisa',
            last_name='farivash',
        )
        self.member_2 = Member(
            title='second_title',
            first_name='sara',
            last_name='amiri',
        )
        self.session.add_all([self.member_1, self.member_2])
