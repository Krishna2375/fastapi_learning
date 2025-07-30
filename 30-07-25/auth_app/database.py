from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , declarative_base
from dotenv import load_dotenv
import os

load_dotenv()
database_url="postgresql://postgres:krishna2005@localhost:5432/employee_db"

engine = create_engine(database_url)
sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()