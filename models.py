import pytest

from sqlalchemy import Column, ForeignKey, \
    Integer, String, create_engine, Date, func, or_, and_, exists
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine(
    'postgresql+psycopg2://postgres:postgres@localhost/practice'
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
        ForeignKey(
            'member.id',
            ondelete='CASCADE',
        ),
    )
    creator = relationship(
        'Member',
        cascade='all,delete',
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
        ForeignKey(
            'member.id',
            ondelete='CASCADE',
        ),
    )
    sender = relationship(
        'Member',
        cascade='all,delete',
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
        ForeignKey(
            'room.id',
            ondelete='CASCADE',
        ),
    )
    room = relationship(
        'Room',
        cascade='all,delete',
        back_populates='messages',
        lazy='joined',
    )


Base.metadata.create_all(bind=engine)


class Config:

    @pytest.fixture
    def setup(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()

        self.session.query(Member).delete()
        self.session.query(Message).delete()
        self.session.query(Room).delete()

        self.member_1 = Member(
            title='first_title',
            first_name='first_name',
            last_name='first_last_name'
        )
        self.session.add(self.member_1)

        self.member_2 = Member(
            title='second_title',
            first_name='second_name',
            last_name='second_last_name'
        )
        self.session.add(self.member_2)

        self.room_1 = Room(
            title='first_room',
        )
        self.session.add(self.room_1)

        self.room_2 = Room(
            title='second_room',
        )
        self.session.add(self.room_2)

        self.message_1 = Message(
            body='first_body',
        )
        self.session.add(self.message_1)

        self.message_2 = Message(
            body='second_body',
        )
        self.session.add(self.message_2)
        self.session.commit()


class Test(Config):

    def test_update(self, setup):
        update_first_name = self.session.query(Member) \
            .filter(Member.id == self.member_1.id) \
            .one()
        update_first_name.first_name = 'edit_first_name'
        self.session.add(update_first_name)
        self.session.commit()
        assert update_first_name.id != None

        update_title_room = self.session.query(Room) \
            .filter(Room.id == self.room_1.id) \
            .one()
        update_title_room.title = 'edit_tittle'
        self.session.add(update_title_room)
        self.session.commit()
        assert update_title_room.id != None

        update_body_message = self.session.query(Message) \
            .filter(Message.id == self.message_1.id) \
            .one()
        update_body_message.body = 'edit_body'
        self.session.add(update_body_message)
        self.session.commit()
        assert update_body_message.id != None

    def test_order_by(self, setup):
        member_order_by_id = self.session.query(Member) \
            .order_by(Member.id) \
            .all()
        assert member_order_by_id[0].id <= member_order_by_id[1].id

        room_order_by_id = self.session.query(Room) \
            .order_by(Room.id) \
            .all()
        assert room_order_by_id[1].id >= room_order_by_id[0].id

        message_order_by_id = self.session.query(Message) \
            .order_by(Message.id). \
            all()
        assert message_order_by_id[0].id <= message_order_by_id[1].id

    def test_exists(self, setup):
        exist_title_with_s = self.session.query(exists() \
            .where(Member.title.startswith('s%'))) \
            .scalar()
        assert exist_title_with_s == True

        exist_room_with_f = self.session.query(exists() \
            .where(Room.title.startswith('f%'))) \
            .scalar()
        assert exist_room_with_f == True

        exist_message_with_p = self.session.query(exists() \
            .where(Message.body.startswith('s%'))) \
            .scalar()
        assert exist_message_with_p == True

    def test_get_member(self, setup):
        get_member = self.session.query(Member) \
            .get(self.member_1.id)
        assert get_member.first_name == 'first_name'

        get_title = self.session.query(Member) \
            .filter(Member.title == 'first_title') \
            .first()
        assert get_title.title == 'first_title'

        check_id = self.session.query(Member) \
            .filter(Member.id == 0) \
            .one_or_none()
        assert check_id == None

    def test_get_room(self, setup):
        room_1 = self.session.query(Room) \
            .get(self.room_1.id)
        assert room_1.title == 'first_room'

        room_1.creator = self.member_1
        self.session.add(room_1)
        self.session.commit()
        assert room_1.creator_id == self.member_1.id

        check_id = self.session.query(Room) \
            .filter(Room.id == 0) \
            .one_or_none()
        assert check_id == None

    def test_get_message(self, setup):
        message_1 = self.session.query(Message) \
            .get(self.message_1.id)
        assert message_1.body == 'first_body'

        message_1.sender_id = self.member_2.id
        self.session.add(message_1)
        self.session.commit()
        assert message_1.sender_id == self.member_2.id

        check_id = self.session.query(Message) \
            .filter(Message.id == 0) \
            .one_or_none()
        assert check_id == None

    def test_limit(self, setup):
        two_limit_member = self.session.query(Member) \
            .limit(2) \
            .all()
        assert len(two_limit_member) == 2

        two_limit_message = self.session.query(Message) \
            .limit(2) \
            .all()
        assert len(two_limit_message) == 2

        two_limit_room = self.session.query(Room) \
            .limit(2) \
            .all()
        assert len(two_limit_room) == 2

    def test_count(self, setup):
        add_title_none = Member(
            first_name='test_name',
            last_name='test_last_name',
        )
        self.session.add(add_title_none)
        self.session.commit()

        exist_none_entity = self.session.query(Member.title) \
            .filter(or_(
                Member.title.is_(None),
                Member.first_name.is_(None),
                Member.last_name.is_(None)
            )) \
            .count()
        assert exist_none_entity == 1

        room_game = self.session.query(Room) \
            .filter(Room.title.match('first_room')) \
            .count()
        assert room_game == 1

        count_messages_of_member = self.session.query(func.count(Member.first_name)) \
            .filter(and_(
                Member.id == Message.sender_id,
                Member.id == self.member_2.id
            )) \
            .scalar()
        assert count_messages_of_member == 0

        count_creator_of_room = self.session.query(func.count(Member.first_name)) \
            .filter(and_(
                Member.id == Room.creator_id,
                Member.id == self.member_1.id
            )) \
            .scalar()
        assert count_creator_of_room == 0

