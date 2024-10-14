from ..config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


class DatabaseHelper:
    def __init__(self, url, echo: bool = False):
        self.engine = create_async_engine(url=url, echo=echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )


db_helper = DatabaseHelper(
    settings.db_url,
    echo=True,
)
