from sqlalchemy import create_engine, Column, Integer, LargeBinary, String, DateTime, desc
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, UTC
from .security import SecurityManager

Base = declarative_base()

class EncryptedMemory(Base):
    __tablename__ = 'memory'
    id = Column(Integer, primary_key=True)
    category = Column(String)  # e.g., 'conversation', 'fact'
    content = Column(LargeBinary)  # Encrypted content
    timestamp = Column(DateTime, default=lambda: datetime.now(UTC))

class MemoryManager:
    def __init__(self, db_url="sqlite:///jarvis_memory.db", security_manager=None):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.security_manager = security_manager or SecurityManager()

    def add_memory(self, category, content):
        session = self.Session()
        encrypted_content = self.security_manager.encrypt(content)
        new_memory = EncryptedMemory(category=category, content=encrypted_content)
        session.add(new_memory)
        session.commit()
        session.close()

    def get_memories(self, category=None, limit=None):
        session = self.Session()
        query = session.query(EncryptedMemory)
        if category:
            query = query.filter(EncryptedMemory.category == category)

        if limit:
            query = query.order_by(desc(EncryptedMemory.timestamp)).limit(limit)
            memories = query.all()
            # Reverse to maintain chronological order for the caller
            memories.reverse()
        else:
            memories = query.all()

        results = []
        for m in memories:
            decrypted_content = self.security_manager.decrypt(m.content)
            results.append({
                'id': m.id,
                'category': m.category,
                'content': decrypted_content,
                'timestamp': m.timestamp
            })
        session.close()
        return results
