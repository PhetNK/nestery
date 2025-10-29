from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

class DatabaseManager:

    def __init__(self, db_name='nestery', user='nestery_db', password='L0g!n', host='192.168.90.102', port=5432):
        db_url = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'
        try:
            self.engine = create_engine(db_url)
            self.Session = sessionmaker(bind=self.engine)
            print("Database engine created.")
        except Exception as e:
            print(f"Error creating engine: {e}")
            self.engine = None

    def is_connect(self) -> bool:
        if not self.engine:
            print("Engine not initialized.")
            return False
        try:
            with self.engine.connect() as conn:
                return True
        except SQLAlchemyError as e:
            print(f"SQLAlchemy error: {e}")
            return False

    def get_session(self):
        if not self.engine:
            raise Exception("Engine not initialized.")
        return self.Session()

    def disconnect(self):
        if self.engine:
            self.engine.dispose()
            print("Engine disposed.")