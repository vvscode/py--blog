import hashlib
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.collections import attribute_mapped_collection

Base = declarative_base()


def generate_password_hash(password):
    m = hashlib.md5()
    m.update(password.encode('utf-8'))
    m.update(m.hexdigest().encode('utf-8'))
    return m.hexdigest()


posts_tags_association = Table(
    "posts_tags",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200))
    login = Column(String(200))
    password_hash = Column(String(128))
    about = Column(String(), unique=True, index=True)
    email = Column(String(50), unique=True, index=True)
    reg_date = Column(DateTime, default=datetime.datetime.now)
    posts = relationship("Post", back_populates="creator")

    def __repr__(self):
        return f"User(id={self.id}, email={self.email})"

    def __init__(self, name, login, password, email):
        self.name = name
        self.login = login
        self.password_hash = generate_password_hash(password)
        self.password = password
        self.email = email

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return generate_password_hash(password) == self.password_hash


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100))
    description = Column(String(1000))
    body = Column(String)

    def __repr__(self):
        return f"Post(id={self.id})"

    creator = relationship("User", back_populates="posts")
    creactor_id = Column(Integer, ForeignKey("users.id"))

    category = relationship("Category", back_populates="posts")
    category_id = Column(Integer, ForeignKey("categories.id"))

    tags = relationship(
        "Tag", secondary=posts_tags_association, back_populates="posts")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    slug = Column(String(100))
    description = Column(String)
    posts = relationship("Post", back_populates="category")

    def __repr__(self):
        return f"Category(id={self.id})"

    # Unfortunately can't fix next
    # "sqlalchemy.exc.NoReferencedTableError: Foreign key associated with column 'categories.parent_id' could not find table 'catogories' with which to generate a foreign key to target column 'id'"
    # # https://stackoverflow.com/questions/4896104/creating-a-tree-from-self-referential-tables-in-sqlalchemy
    # parent_id = Column(Integer, ForeignKey("catogories.id"))
    # children = relationship(
    #     "Category",
    #     cascade="all",
    #     backref=backref("parent", remote_side="categories.parent_id"),
    #     collection_class=attribute_mapped_collection("name"),
    # )

    # def __init__(self, name, parent=None):
    #     self.name = name
    #     self.parent = parent

    # def append(self, nodename):
    #     self.children[nodename] = Category(nodename, parent=self)


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    slug = Column(String(100))
    description = Column(String)

    def __repr__(self):
        return f"Category(id={self.id})"

    posts = relationship(
        "Post", secondary=posts_tags_association, back_populates="tags"
    )
