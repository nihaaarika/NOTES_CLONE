import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import bcrypt

class NotesDatabase:
    """Professional database handler for Secret Diary"""

    def __init__(self, db_path: str = "data/notes.db"):
        self.db_path = db_path
        Path("data").mkdir(exist_ok=True)
        self.init_db()

    def get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone TEXT,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Journal entries table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS journal_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                entry_date DATE,
                title TEXT,
                content TEXT,
                font_family TEXT DEFAULT 'Lora',
                text_color TEXT DEFAULT '#1e293b',
                bg_color TEXT DEFAULT '#ffffff',
                bg_theme TEXT DEFAULT 'minimal',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)

        # Voice notes (Secret Talk) table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS voice_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                entry_date DATE,
                audio_filename TEXT,
                transcription TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)

        # Manifestations (Goals) table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS manifestations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                goal_text TEXT NOT NULL,
                completed INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)

        # Everyday notes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS everyday_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                note_date DATE,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)

        conn.commit()
        conn.close()

    # ========== USER OPERATIONS ==========

    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode()

    def verify_password(self, password: str, hash_str: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode(), hash_str.encode())

    def create_user(self, name: str, email: str, phone: str, password: str) -> int:
        """Create a new user"""
        conn = self.get_connection()
        cursor = conn.cursor()

        password_hash = self.hash_password(password)

        try:
            cursor.execute("""
                INSERT INTO users (name, email, phone, password_hash)
                VALUES (?, ?, ?, ?)
            """, (name, email, phone, password_hash))

            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return user_id
        except sqlite3.IntegrityError:
            conn.close()
            return None

    def verify_user(self, email: str, password: str) -> Optional[Dict]:
        """Verify user credentials"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, name, email, password_hash FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        conn.close()

        if row and self.verify_password(password, row['password_hash']):
            return {'id': row['id'], 'name': row['name'], 'email': row['email']}
        return None

    # ========== JOURNAL OPERATIONS ==========

    def create_journal_entry(self, user_id: int, title: str, content: str, font_family: str = "Lora",
                            text_color: str = "#1e293b", bg_color: str = "#ffffff",
                            bg_theme: str = "minimal") -> int:
        """Create a journal entry"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO journal_entries (user_id, entry_date, title, content, font_family, text_color, bg_color, bg_theme)
            VALUES (?, DATE('now'), ?, ?, ?, ?, ?, ?)
        """, (user_id, title, content, font_family, text_color, bg_color, bg_theme))

        entry_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return entry_id

    def get_journal_entries(self, user_id: int) -> List[Dict]:
        """Get all journal entries for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM journal_entries
            WHERE user_id = ?
            ORDER BY entry_date DESC
        """, (user_id,))

        entries = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return entries

    def get_journal_entry(self, entry_id: int) -> Optional[Dict]:
        """Get a specific journal entry"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM journal_entries WHERE id = ?", (entry_id,))
        row = cursor.fetchone()
        conn.close()

        return dict(row) if row else None

    def update_journal_entry(self, entry_id: int, title: str = None, content: str = None,
                            font_family: str = None, text_color: str = None,
                            bg_color: str = None, bg_theme: str = None):
        """Update a journal entry"""
        conn = self.get_connection()
        cursor = conn.cursor()

        updates = []
        params = []

        if title is not None:
            updates.append("title = ?")
            params.append(title)
        if content is not None:
            updates.append("content = ?")
            params.append(content)
        if font_family is not None:
            updates.append("font_family = ?")
            params.append(font_family)
        if text_color is not None:
            updates.append("text_color = ?")
            params.append(text_color)
        if bg_color is not None:
            updates.append("bg_color = ?")
            params.append(bg_color)
        if bg_theme is not None:
            updates.append("bg_theme = ?")
            params.append(bg_theme)

        if updates:
            updates.append("updated_at = CURRENT_TIMESTAMP")
            query = f"UPDATE journal_entries SET {', '.join(updates)} WHERE id = ?"
            params.append(entry_id)
            cursor.execute(query, params)
            conn.commit()

        conn.close()

    def delete_journal_entry(self, entry_id: int):
        """Delete a journal entry"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM journal_entries WHERE id = ?", (entry_id,))
        conn.commit()
        conn.close()

    # ========== VOICE NOTES OPERATIONS ==========

    def create_voice_note(self, user_id: int, audio_filename: str, transcription: str = "") -> int:
        """Create a voice note"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO voice_notes (user_id, entry_date, audio_filename, transcription)
            VALUES (?, DATE('now'), ?, ?)
        """, (user_id, audio_filename, transcription))

        note_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return note_id

    def get_voice_notes(self, user_id: int) -> List[Dict]:
        """Get all voice notes for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM voice_notes
            WHERE user_id = ?
            ORDER BY entry_date DESC
        """, (user_id,))

        notes = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return notes

    def delete_voice_note(self, note_id: int):
        """Delete a voice note"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM voice_notes WHERE id = ?", (note_id,))
        conn.commit()
        conn.close()

    # ========== MANIFESTATIONS OPERATIONS ==========

    def create_manifestation(self, user_id: int, goal_text: str) -> int:
        """Create a manifestation/goal"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO manifestations (user_id, goal_text)
            VALUES (?, ?)
        """, (user_id, goal_text))

        goal_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return goal_id

    def get_manifestations(self, user_id: int, completed_only: bool = False) -> List[Dict]:
        """Get all manifestations for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()

        if completed_only:
            query = "SELECT * FROM manifestations WHERE user_id = ? AND completed = 1 ORDER BY updated_at DESC"
        else:
            query = "SELECT * FROM manifestations WHERE user_id = ? ORDER BY completed, updated_at DESC"

        cursor.execute(query, (user_id,))
        goals = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return goals

    def update_manifestation(self, goal_id: int, completed: int = None, goal_text: str = None):
        """Update a manifestation"""
        conn = self.get_connection()
        cursor = conn.cursor()

        updates = []
        params = []

        if completed is not None:
            updates.append("completed = ?")
            params.append(completed)
        if goal_text is not None:
            updates.append("goal_text = ?")
            params.append(goal_text)

        if updates:
            updates.append("updated_at = CURRENT_TIMESTAMP")
            query = f"UPDATE manifestations SET {', '.join(updates)} WHERE id = ?"
            params.append(goal_id)
            cursor.execute(query, params)
            conn.commit()

        conn.close()

    def delete_manifestation(self, goal_id: int):
        """Delete a manifestation"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM manifestations WHERE id = ?", (goal_id,))
        conn.commit()
        conn.close()

    # ========== EVERYDAY NOTES OPERATIONS ==========

    def create_everyday_note(self, user_id: int, content: str) -> int:
        """Create an everyday note"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO everyday_notes (user_id, note_date, content)
            VALUES (?, DATE('now'), ?)
        """, (user_id, content))

        note_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return note_id

    def get_everyday_notes(self, user_id: int) -> List[Dict]:
        """Get all everyday notes for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM everyday_notes
            WHERE user_id = ?
            ORDER BY note_date DESC
        """, (user_id,))

        notes = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return notes

    def get_everyday_note_by_date(self, user_id: int, date: str) -> Optional[Dict]:
        """Get everyday note for a specific date"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM everyday_notes
            WHERE user_id = ? AND note_date = ?
        """, (user_id, date))

        row = cursor.fetchone()
        conn.close()

        return dict(row) if row else None

    def update_everyday_note(self, note_id: int, content: str):
        """Update an everyday note"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE everyday_notes
            SET content = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (content, note_id))

        conn.commit()
        conn.close()

    def delete_everyday_note(self, note_id: int):
        """Delete an everyday note"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM everyday_notes WHERE id = ?", (note_id,))
        conn.commit()
        conn.close()

# Initialize database on import
db = NotesDatabase()