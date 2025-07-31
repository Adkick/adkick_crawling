from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import MYSQL_BINDING_PORT, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE

SQLALCHEMY_DATABASE_URL = f"mysql+mysqldb://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_BINDING_PORT}/{MYSQL_DATABASE}"
print(SQLALCHEMY_DATABASE_URL)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=10,
    max_overflow=20,
    connect_args={
        "connect_timeout": 30,
        "read_timeout": 30,
        "write_timeout": 30,
        "unix_socket": "",
    }
)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()