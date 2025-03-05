from contextlib import contextmanager
import logging
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base


from src.models.settings import FINANCIAL_DATA_DB, FINANCIAL_DATA_DB_SCHEMA


engine = create_engine(FINANCIAL_DATA_DB, pool_pre_ping=True)

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False))

Base = declarative_base(metadata=MetaData(schema=FINANCIAL_DATA_DB_SCHEMA))

logging.basicConfig(level=logging.INFO)


class BaseModel(Base):
    """Base model class that includes session management."""
    __abstract__ = True

    logger = logging.getLogger(__name__)

    @classmethod
    @contextmanager
    def get_session(cls):
        """Context manager for database session handling."""
        session = SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            cls.logger.error(f"Database transaction failed: {e}")
            raise
        finally:
            session.close()
            SessionLocal.remove()
