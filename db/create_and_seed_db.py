from sqlalchemy.orm import scoped_session, sessionmaker, relationship

from db_declaration import Base, User, Post, Category, Tag
from db import engine

Base.metadata.bind = engine
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = scoped_session(Session)


def create_db():
    Base.metadata.create_all()


def seed_db():
    tags = []

    for category_name in ['category1', 'category2']:
        category = Category(
            name=category_name,
            slug=f'slug_for_{category_name}',
            description=f'description_for_{category_name}'
        )
        session.add(category)

    for tag_name in ['tag1', 'tag2', 'tag3']:
        tag = Tag(
            name=tag_name,
            slug=f'slug_for_{tag_name}',
            description=f'description_for_{tag_name}'
        )
        tags.append(tag)
        session.add(tag)

    for user_name in ['Bob', 'Sam']:
        user = User(
            login=user_name,
            name=user_name,
            password=f'pass for {user_name}',
            email=f'{user_name}@me',
        )
        session.add(user)

    post = Post(
        title='Some post',
        description='Some description',
        body='Some body',
        creator=user,
        category=category,
    )

    post.tags = tags[1:]
    session.add(post)

    session.commit()


# looks like it worth to use `alembic` or something like that
if __name__ == '__main__':
    create_db()
    seed_db()
