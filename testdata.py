import random
import string

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from catalog_app.api.util import encrypt_password, check_password
from catalog_app.api.models import Base, User, Category, Item

from settings import config


engine = create_engine(
    config.DATABASE_URI
)
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()


def generate_token(length=12):
    return ''.join(random.choice(string.ascii_uppercase+string.digits)
                   for x in xrange(length))

# Create dummy user
for i in range(10):
    password = "user{}password".format(i + 1)
    enc, salt = encrypt_password(password)
    user = User(name="user{}".format(i + 1),
                email="user{}@email.com".format(i + 1),
                password=enc, salt=salt)
    session.add(user)
    session.commit()

for c in range(10):
    category = Category(name="category{}".format(c + 1))
    session.add(category)
    session.commit()

    for i in range(10):
        item = Item(title="item{}_c{}".format(i + 1, c + 1),
                    category_id=category.id, user_id=(i % 10 + 1))
        item.description = "This is a description of category: \
        {} and item: {}. This item is created by {}"\
            .format(i + 1, c + 1, "user{}".format(i % 10 + 1))
        session.add(item)
        session.commit()

print "inserting rows done!"
