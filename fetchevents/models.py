from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy import (
        Column, Integer, String, Date, UnicodeText, ForeignKey, Table
        )

Base = declarative_base()
Session = sessionmaker()
engine = create_engine('sqlite:///events.db', echo=False)
Session.configure(bind=engine)
session = Session()

# m2m table
event_tags = Table('event_tag', Base.metadata,
    Column('event_id', ForeignKey('events.id'), primary_key=True),
    Column('tag_id', ForeignKey('tags.id'), primary_key=True)
)


class Event(Base):
    """Parsed Event"""
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(UnicodeText)
    location = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    url = Column(String)
    source = Column(String)
    image_link = Column(String)
    tags = relationship('Tag',
        secondary=event_tags,
        back_populates='events')

    def __repr__(self):
        return "Event: {}".format(self.title.encode('utf8'))


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    events = relationship('Event',
        secondary=event_tags,
        back_populates='tags')

    def __repr__(self):
        return "Tag: {}".format(self.title.encode('utf8'))

Base.metadata.create_all(engine)
