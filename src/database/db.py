from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from src.conf.config import settings

URI = settings.sqlalchemy_database_url

engine = create_engine(URI, echo=False, pool_size=5)

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Dependency


def get_db():
    db = DBSession()
    try:
        yield db
    except SQLAlchemyError as err:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    finally:
        db.close()




# import configparser
# import pathlib
# from fastapi import HTTPException, status

# from sqlalchemy import create_engine
# from sqlalchemy.exc import SQLAlchemyError
# from sqlalchemy.orm import sessionmaker

# file_config = pathlib.Path(__file__).parent.parent.joinpath('conf/config_111.ini')
# config = configparser.ConfigParser()
# config.read(file_config)

# username = config.get('DB', 'user')
# password = config.get('DB', 'pass')
# db_name = config.get('DB', 'db_name')
# domain = config.get('DB', 'domain')
# port = config.get('DB', 'port')

# URI = f'postgresql://{username}:{password}@{domain}:{port}/{db_name}'

# engine = create_engine(URI, echo=True)

# DBSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# def get_db():
#     db = DBSession()
#     try:
#         yield db
#     except SQLAlchemyError as err:
#         db.rollback()
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
#     finally:
#         db.close()