from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL format:
# mysql+pymysql://<username>:<password>@<host>/<db_name>
# Since XAMPP default is usually 'root' with no password, we leave it empty after the colon.

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost:3306/barangay_system_db"

# Create the engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a SessionLocal class
# Each instance of this class will be a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class
# All our models will inherit from this class
Base = declarative_base()

# Dependency: This function will be used in FastAPI endpoints to get a db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()