from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Resolvo ticket-galai save panna oru local database file create pandrom
SQLALCHEMY_DATABASE_URL = "sqlite:///./resolvo.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
# Tables-ah create panna intha line mukkiyam
def init_db():
    Base.metadata.create_all(bind=engine)
 #   git add .
#git commit -m "Add database table creation command"
#
# git push origin main