from sqlalchemy import Column, ForeignKey, \
    Integer, String, create_engine, Date, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(
    "postgresql+psycopg2://postgres:postgres@localhost/sqlalchemy_practice"
)
Base = declarative_base()


members_room = Table('members_room', Base.metadata,
    Column('member_id', ForeignKey('member.id')),
    Column('room_id', ForeignKey('room.id'))
)


class Member(Base):
    __tablename__ = 'member'

    id = Column(Integer, primary_key=True)
    title = Column('title', String)
    first_name = Column('first_name', String)
    last_name = Column('last_name', String)
    birthday = Column('birthday', Date)
    rooms = relationship(
        'Room',
        back_populates='member',
        lazy='joined'
    )


class Room(Base):
    __tablename__ = 'room'

    id = Column(Integer, primary_key=True)
    title = Column('title', String)
    creator_id = Column('creator_id', Integer, ForeignKey('member.id'))
    members = relationship(
        'Member',
        order_by='room.id',
        secondary=members_room,
        back_populates='rooms',
        lazy='joined'
    )
