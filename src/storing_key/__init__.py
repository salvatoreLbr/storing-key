from src.storing_key.db import models
from src.storing_key.db.database import SessionLocal, engine

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()
