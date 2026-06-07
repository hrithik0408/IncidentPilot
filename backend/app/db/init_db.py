from app.db.session import Base, engine
from app.models import models  # noqa

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Database tables ensured.")
