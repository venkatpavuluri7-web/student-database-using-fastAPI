from sqlalchemy import create_engine
from urllib.parse import quote_plus
from sqlalchemy.orm import declarative_base,sessionmaker
from config import settings
database_url=(f"mysql+pymysql://{quote_plus(settings.db_user)}:{quote_plus(settings.db_password)}"
f"@{settings.db_host}:{settings.db_port}"
f"/{settings.db_name}")
engine=create_engine(database_url,echo=True)
Base=declarative_base()
SessionLocal=sessionmaker(autocommit=False,
                          autoflush=False,
                          bind=engine)
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


