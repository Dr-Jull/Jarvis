import unittest
import os
import sqlite3
from src.security import SecurityManager
from src.memory import MemoryManager
from src.jarvis import JARVIS
from src.llm import MockLLM

class TestJARVIS(unittest.TestCase):
    def setUp(self):
        self.key_path = "test_key.key"
        self.db_url = "sqlite:///test_memory.db"
        self.security = SecurityManager(key_path=self.key_path)
        self.memory = MemoryManager(db_url=self.db_url, security_manager=self.security)
        self.jarvis = JARVIS(memory_manager=self.memory, llm_provider=MockLLM())

    def tearDown(self):
        if os.path.exists(self.key_path):
            os.remove(self.key_path)
        if os.path.exists("test_memory.db"):
            os.remove("test_memory.db")

    def test_encryption_decryption(self):
        original_text = "Secret memory"
        encrypted = self.security.encrypt(original_text)
        self.assertNotEqual(original_text, encrypted)
        decrypted = self.security.decrypt(encrypted)
        self.assertEqual(original_text, decrypted)

    def test_memory_is_encrypted_in_db(self):
        secret_fact = "Tony Stark's favorite color is red"
        self.jarvis.remember_fact(secret_fact)

        # Manually check the database content
        conn = sqlite3.connect("test_memory.db")
        cursor = conn.cursor()
        cursor.execute("SELECT content FROM memory")
        rows = cursor.fetchall()
        conn.close()

        self.assertTrue(len(rows) > 0)
        encrypted_content = rows[0][0]

        # Verify it's encrypted (not plain text)
        self.assertNotIn(secret_fact.encode(), encrypted_content)

        # Verify we can decrypt it back
        decrypted_content = self.security.decrypt(encrypted_content)
        self.assertEqual(secret_fact, decrypted_content)

    def test_jarvis_interaction(self):
        response = self.jarvis.ask("What is your name?")
        self.assertIn("JARVIS", response)

        memories = self.memory.get_memories(category="conversation")
        self.assertTrue(any("What is your name?" in m['content'] for m in memories))
        self.assertTrue(any(response in m['content'] for m in memories))

if __name__ == "__main__":
    unittest.main()
