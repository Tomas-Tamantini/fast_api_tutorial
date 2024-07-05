from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fast_api_tutorial.persistence.unit_of_work import UnitOfWork
from fast_api_tutorial.persistence.relational import RelationalUnitOfWork
from fast_api_tutorial.settings import Settings


def get_unit_of_work() -> UnitOfWork:
    db_url = Settings().DATABASE_URL
    engine = create_engine(db_url)
    session_factory = sessionmaker(bind=engine)
    return RelationalUnitOfWork(session_factory)
