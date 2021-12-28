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
        cascade="all,delete",
        back_populates='creator_room',
        lazy='joined',
    )
    messages = relationship(
        'Message',
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
        cascade="all,delete",
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
        cascade="all,delete",
        back_populates='messages',
        lazy='joined',
    )


Base.metadata.create_all(bind=engine)


class Config:

    @pytest.fixture
    def setup(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()

        # self.session.query(Member).delete()
        # self.session.query(Message).delete()
        # self.session.query(Room).delete()

        self.member_1 = Member(
            title='first_title',
            first_name='parisa',
            last_name='farivash'
        )
        self.member_2 = Member(
            title='second_title',
            first_name='sara',
            last_name='amiri'
        )
        self.session.add_all([self.member_1, self.member_2])

        self.room_1 = Room(
            title='first_room',
        )
        self.room_2 = Room(
            title='second_room',
        )
        self.session.add_all([self.room_1, self.room_2])

        self.message_1 = Message(
            body='Hi',
        )
        self.message_2 = Message(
            body='Ok',
        )
        self.session.add_all([self.message_1, self.message_2])
        self.session.commit()


class TestQuery(Config):

    def test_member(self, setup):
        member = self.session.query(Member).get(self.member_1.id)
        assert member.first_name == 'parisa'

        first_title = self.session.query(Member).filter(Member.title == 'first_title').first()
        assert first_title.title == 'first_title'

    def test_room(self, setup):
        room_1 = self.session.query(Room).get(self.room_1.id)
        assert room_1.title == 'first_room'

        room_1.creator = self.member_1
        self.session.add(room_1)
        self.session.commit()
        assert room_1.creator_id == self.member_1.id

    def test_message(self, setup):
        message_1 = self.session.query(Message).get(self.message_1.id)
        assert message_1.body == 'Hi'

        message_1.sender_id = self.member_2.id
        self.session.add(message_1)
        self.session.commit()

        assert message_1.sender_id == self.member_2.id


