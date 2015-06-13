import datetime

from sqlalchemy import asc, desc
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    password = Column(String)
    salt = Column(String)
    name = Column(String)
    picture = Column(String)
    created = Column(DateTime(timezone=True),
                     default=datetime.datetime.utcnow())

    @classmethod
    def get_by_id(cls, session, id):
        User = cls
        try:
            user = session.query(User).filter_by(id=id).one()
        except:
            user = None
        return user

    @classmethod
    def get_by_email(cls, session, email):
        User = cls
        try:
            user = session.query(User).filter_by(email=email).one()
        except:
            user = None
        return user

    @classmethod
    def is_authorized(cls, session, user_id, item_id):
        try:
            item = session.query(Item).filter_by(id=item_id).one()
            return user_id == item.user_id

        except:
            return False


class Category(Base):

    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created = Column(DateTime(timezone=True),
                     default=datetime.datetime.utcnow())

    @classmethod
    def get_all(cls, session, order_by=None, ascending=True):
        Category = cls
        if order_by is not None:
            if asc:
                categories = session.query(Category)\
                    .order_by(asc(order_by)).all()
            else:
                categories = session.query(Category)\
                    .order_by(desc(order_by)).all()
        else:
            categories = session.query(Category).all()
        return categories

    @classmethod
    def get_by_id(cls, session, id):
        Category = cls
        try:
            category = session.query(Category)\
                .filter_by(id=id).one()
        except:
            category = None
        return category

    @classmethod
    def item_set(cls, session, category_id):
        try:
            items = session.query(Item)\
                .filter_by(category_id=category_id)
        except:
            items = []
        return items

    @property
    def serialize(self):

        return {
            'id': self.id,
            'name': self.name,
            'created': self.created
        }


class Item(Base):

    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    price = Column(String)
    category_id = Column(
        Integer, ForeignKey('category.id')
    )
    category = relationship(Category)
    user_id = Column(
        Integer, ForeignKey('user.id')
    )
    user = relationship(User)
    created = Column(DateTime(timezone=True),
                     default=datetime.datetime.utcnow())

    @classmethod
    def get_recent(cls, session, limit=10):
        Item = cls
        items = session.query(Item)\
            .order_by(desc(Item.created), desc(Item.id)).limit(limit)
        return items

    @classmethod
    def get_by_id(cls, session, id):
        Item = cls
        try:
            item = session.query(Item).filter_by(id=id).one()
        except:
            item = None
        return item

    @property
    def serialize(self):

        return {
            'title': self.title,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'category_id': self.category_id,
            'user_id': self.user_id,
            'created': self.created
        }
