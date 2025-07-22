from app.database import engine, Base
from app.models import user  # ensure user model is registered
from app.models import calculation  # ensure calculation model is registered

def init_db():
    Base.metadata.create_all(bind=engine)

def drop_db():
    Base.metadata.drop_all(bind=engine)

if __name__ == "__main__":
    init_db()  # pragma: no cover