import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool
from .models import Base


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://taskuser:secret@localhost:5432/taskdb"
)

# Настройки подключения
engine_kwargs = {
    "pool_size": 10,           
    "max_overflow": 20,        
    "pool_pre_ping": True,     
    "echo": os.getenv("SQL_ECHO", "False").lower() == "true",  
}

# Создание движка SQLAlchemy
engine = create_engine(DATABASE_URL, **engine_kwargs)

# Фабрика сессий
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def init_db():

    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        raise

def get_db() -> Session:

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def check_db_connection() -> bool:

    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False

def get_db_stats() -> dict:

    from sqlalchemy import text
    
    try:
        db = SessionLocal()
        result = db.execute(text("""
            SELECT 
                count(*) as active_connections,
                (SELECT count(*) FROM pg_stat_activity 
                 WHERE datname = current_database()) as total_connections
        """))
        stats = result.mapping().first()
        db.close()
        return dict(stats) if stats else {}
    except Exception as e:
        return {"error": str(e)}