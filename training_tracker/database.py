import databases
import sqlalchemy
from sqlalchemy import sql

from training_tracker.config import config

metadata = sqlalchemy.MetaData()

distances = sqlalchemy.Table(
    "distances",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("distance", sqlalchemy.Numeric),
    sqlalchemy.Column("units", sqlalchemy.String),
    sqlalchemy.Column(
        "added_by_user_id",
        sqlalchemy.ForeignKey("users.id", ondelete="SET NULL"),
        nullable=False,
    ),
)

groups = sqlalchemy.Table(
    "groups",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column(
        "added_by_user_id",
        sqlalchemy.ForeignKey("users.id", ondelete="SET NULL"),
        nullable=False,
    ),
)

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True),
    sqlalchemy.Column("password", sqlalchemy.String),
    sqlalchemy.Column("confirmed", sqlalchemy.Boolean, server_default=sql.false()),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=sql.func.now()),
)

weights = sqlalchemy.Table(
    "weights",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("weight", sqlalchemy.Numeric),
    sqlalchemy.Column("units", sqlalchemy.String),
    sqlalchemy.Column(
        "added_by_user_id",
        sqlalchemy.ForeignKey("users.id", ondelete="SET NULL"),
        nullable=False,
    ),
)

exersices = sqlalchemy.Table(
    "exersices",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column(
        "group_id",
        sqlalchemy.ForeignKey("groups.id", ondelete="SET NULL"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "added_by_user_id",
        sqlalchemy.ForeignKey("users.id", ondelete="SET NULL"),
        nullable=False,
    ),
)

trainings = sqlalchemy.Table(
    "trainings",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "training_date", sqlalchemy.Date, server_default=sql.func.current_date()
    ),
    sqlalchemy.Column("status", sqlalchemy.String, server_default="Started"),
    sqlalchemy.Column(
        "user_id",
        sqlalchemy.ForeignKey("users.id", ondelete="SET NULL"),
        nullable=False,
    ),
)

sets = sqlalchemy.Table(
    "sets",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("exercise_count", sqlalchemy.Integer),
    sqlalchemy.Column(
        "exercise_id",
        sqlalchemy.ForeignKey("exersices.id", ondelete="CASCADE"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "training_id",
        sqlalchemy.ForeignKey("trainings.id", ondelete="CASCADE"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "distance_id",
        sqlalchemy.ForeignKey("distances.id", ondelete="CASCADE"),
        nullable=True,
    ),
    sqlalchemy.Column(
        "weight_id",
        sqlalchemy.ForeignKey("weights.id", ondelete="CASCADE"),
        nullable=True,
    ),
    sqlalchemy.Column(
        "added_by_user_id",
        sqlalchemy.ForeignKey("users.id", ondelete="SET NULL"),
        nullable=False,
    ),
)

connect_args = {"check_same_thread": False} if "sqlite" in config.DATABASE_URL else {}

engine = sqlalchemy.create_engine(config.DATABASE_URL, connect_args=connect_args)


db_args = {"min_size": 1, "max_size": 3} if "postgres" in config.DATABASE_URL else {}
database = databases.Database(
    config.DATABASE_URL, force_rollback=config.DB_FORCE_ROLL_BACK, **db_args
)
