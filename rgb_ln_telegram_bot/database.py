"""Database models module."""
import datetime
import enum

from sqlalchemy import DATETIME, Enum, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    mapped_column,
    relationship,
    scoped_session,
    sessionmaker,
)


class SendRequestStatus(enum.Enum):
    """Status of a SendRequest entry."""

    PENDING = 0
    RGB_INVOICE_ALREADY_USED = 1
    SUCCESS = 2


class PurchaseStatus(enum.Enum):
    """Status of a Purchase entry."""

    PENDING = 0
    DELIVERED = 1
    EXPIRED = 2
    FAILED = 3


# pylint: disable=too-few-public-methods,super-init-not-called


class Base(DeclarativeBase):
    """Base for new declarative mappings."""


class Purchase(Base):
    """DB table representing a LN purchase."""

    __tablename__ = "purchase"

    idx = mapped_column(Integer, primary_key=True)
    invoice = mapped_column(String(256), nullable=False)
    status = mapped_column(Enum(PurchaseStatus), nullable=False)
    chat_id = mapped_column(Integer, nullable=False)

    def __init__(self, invoice, chat_id):
        """Instantiate a Purchase."""
        self.invoice = invoice
        self.status = PurchaseStatus.PENDING
        self.chat_id = chat_id


class SendRequest(Base):
    """DB table representing a request for some on-chain assets."""

    __tablename__ = "sendrequest"

    idx = mapped_column(Integer, primary_key=True)
    user_idx = mapped_column(Integer, ForeignKey("user.idx"), nullable=False)
    txid = mapped_column(String(256), nullable=True)
    timestamp = mapped_column(DATETIME, nullable=False)
    rgb_invoice = mapped_column(String(256), nullable=True)
    status = mapped_column(Enum(SendRequestStatus), nullable=False)

    def __init__(self, user_idx):
        """Instantiate a SendRequest."""
        self.user_idx = user_idx
        self.status = SendRequestStatus.PENDING
        self.timestamp = datetime.datetime.now()
        self.rgb_invoice = None


class User(Base):
    """DB table representing a user of the bot."""

    __tablename__ = "user"

    idx = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, nullable=False)
    sendrequest = relationship("SendRequest")  # noqa: F841

    def __init__(self, user_id):
        """Instantiate a User."""
        self.user_id = user_id


# pylint: enable=too-few-public-methods


def init_db_session(database_uri):
    """Initialize the database."""
    engine = create_engine(database_uri)
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    return scoped_session(session_factory)
