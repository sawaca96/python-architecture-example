from typing import Tuple

import sqlalchemy as sa

metadata = sa.MetaData()


def timestamps() -> Tuple[sa.Column, sa.Column]:
    return (
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
            onupdate=sa.func.current_timestamp(),
        ),
    )


user = sa.Table(
    "user",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("username", sa.Text, unique=True, nullable=False, index=True),
    sa.Column("email", sa.Text, unique=True, nullable=False, index=True),
    sa.Column("password", sa.Text),
    sa.Column("bio", sa.Text),
    sa.Column("image", sa.Text),
    *timestamps(),
)

follower_x_following = (
    sa.Table(
        "follower_x_following",
        metadata,
        sa.Column(
            "follower_id",
            sa.Integer,
            sa.ForeignKey("user.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "following_id",
            sa.Integer,
            sa.ForeignKey("user.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint(
            "follower_id",
            "following_id",
            name="pk_follower_x_following",
        ),
    ),
)


article = sa.Table(
    "article",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("slug", sa.Text, unique=True, nullable=False, index=True),
    sa.Column("title", sa.Text, nullable=False),
    sa.Column("description", sa.Text, nullable=False),
    sa.Column("body", sa.Text, nullable=False),
    sa.Column("author_id", sa.Integer, sa.ForeignKey("user.id", ondelete="SET NULL")),
    *timestamps(),
)

tag = sa.Table("tag", metadata, sa.Column("name", sa.Text, primary_key=True))

article_x_tag = sa.Table(
    "article_x_tag",
    metadata,
    sa.Column(
        "article_id",
        sa.Integer,
        sa.ForeignKey("article.id", ondelete="CASCADE"),
        nullable=False,
    ),
    sa.Column(
        "tag",
        sa.Text,
        sa.ForeignKey("tag.name", ondelete="CASCADE"),
        nullable=False,
    ),
    sa.PrimaryKeyConstraint("article_id", "tag", name="pk_article_x_tag"),
)

favorite_article = sa.Table(
    "favorite_article",
    metadata,
    sa.Column(
        "user_id",
        sa.Integer,
        sa.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    ),
    sa.Column(
        "article_id",
        sa.Integer,
        sa.ForeignKey("article.id", ondelete="CASCADE"),
        nullable=False,
    ),
    sa.PrimaryKeyConstraint("user_id", "article_id", name="pk_favorite_article"),
)

comment = sa.Table(
    "comment",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("body", sa.Text, nullable=False),
    sa.Column(
        "author_id",
        sa.Integer,
        sa.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    ),
    sa.Column(
        "article_id",
        sa.Integer,
        sa.ForeignKey("article.id", ondelete="CASCADE"),
        nullable=False,
    ),
    *timestamps(),
)
