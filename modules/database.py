import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple

class NotesDatabase:
    """Professional database handler for notes, todos, and diary entries"""
    
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
        
        # Notes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                tags TEXT DEFAULT '[]',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                color TEXT DEFAULT '#ffffff',
                pinned INTEGER DEFAULT 0
            )
        """)
        
        # Todo List table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                completed INTEGER DEFAULT 0,
                due_date DATE,
                priority TEXT DEFAULT 'medium',
                category TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Diary Entries table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS diary_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entry_date DATE NOT NULL UNIQUE,
                title TEXT,
                content TEXT,
                mood TEXT DEFAULT 'neutral',
                tags TEXT DEFAULT '[]',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # User preferences table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                theme TEXT DEFAULT 'light',
                accent_color TEXT DEFAULT '#6366f1',
                font_size INTEGER DEFAULT 16,
                auto_save INTEGER DEFAULT 1
            )
        """)
        
        conn.commit()
        conn.close()
    
    # ========== NOTES OPERATIONS ==========
    
    def create_note(self, title: str, content: str = "", tags: List[str] = None, color: str = "#ffffff") -> int:
        """Create a new note"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        tags = tags or []
        cursor.execute("""
            INSERT INTO notes (title, content, tags, color)
            VALUES (?, ?, ?, ?)
        """, (title, content, json.dumps(tags), color))
        
        note_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return note_id
    
    def get_all_notes(self, search: str = "") -> List[Dict]:
        """Get all notes, optionally filtered by search"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if search:
            query = """
                SELECT * FROM notes 
                WHERE title LIKE ? OR content LIKE ?
                ORDER BY pinned DESC, updated_at DESC
            """
            cursor.execute(query, (f"%{search}%", f"%{search}%"))
        else:
            query = "SELECT * FROM notes ORDER BY pinned DESC, updated_at DESC"
            cursor.execute(query)
        
        notes = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        # Parse tags from JSON
        for note in notes:
            note['tags'] = json.loads(note.get('tags', '[]'))
        
        return notes
    
    def get_note(self, note_id: int) -> Optional[Dict]:
        """Get a specific note"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            note = dict(row)
            note['tags'] = json.loads(note.get('tags', '[]'))
            return note
        return None
    
    def update_note(self, note_id: int, title: str = None, content: str = None, 
                   tags: List[str] = None, color: str = None, pinned: int = None):
        """Update a note"""
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
        if tags is not None:
            updates.append("tags = ?")
            params.append(json.dumps(tags))
        if color is not None:
            updates.append("color = ?")
            params.append(color)
        if pinned is not None:
            updates.append("pinned = ?")
            params.append(pinned)
        
        if updates:
            updates.append("updated_at = CURRENT_TIMESTAMP")
            query = f"UPDATE notes SET {', '.join(updates)} WHERE id = ?"
            params.append(note_id)
            cursor.execute(query, params)
            conn.commit()
        
        conn.close()
    
    def delete_note(self, note_id: int):
        """Delete a note"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        conn.commit()
        conn.close()
    
    # ========== TODO OPERATIONS ==========
    
    def create_todo(self, title: str, description: str = "", due_date: str = None, 
                   priority: str = "medium", category: str = None) -> int:
        """Create a new todo"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO todos (title, description, due_date, priority, category)
            VALUES (?, ?, ?, ?, ?)
        """, (title, description, due_date, priority, category))
        
        todo_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return todo_id
    
    def get_all_todos(self, filter_completed: bool = False) -> List[Dict]:
        """Get all todos, optionally filtered"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if filter_completed:
            query = "SELECT * FROM todos WHERE completed = 0 ORDER BY due_date, priority DESC"
        else:
            query = "SELECT * FROM todos ORDER BY completed, due_date, priority DESC"
        
        cursor.execute(query)
        todos = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return todos
    
    def get_todo(self, todo_id: int) -> Optional[Dict]:
        """Get a specific todo"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    def update_todo(self, todo_id: int, title: str = None, description: str = None, 
                   completed: int = None, due_date: str = None, 
                   priority: str = None, category: str = None):
        """Update a todo"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if title is not None:
            updates.append("title = ?")
            params.append(title)
        if description is not None:
            updates.append("description = ?")
            params.append(description)
        if completed is not None:
            updates.append("completed = ?")
            params.append(completed)
        if due_date is not None:
            updates.append("due_date = ?")
            params.append(due_date)
        if priority is not None:
            updates.append("priority = ?")
            params.append(priority)
        if category is not None:
            updates.append("category = ?")
            params.append(category)
        
        if updates:
            updates.append("updated_at = CURRENT_TIMESTAMP")
            query = f"UPDATE todos SET {', '.join(updates)} WHERE id = ?"
            params.append(todo_id)
            cursor.execute(query, params)
            conn.commit()
        
        conn.close()
    
    def delete_todo(self, todo_id: int):
        """Delete a todo"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        conn.commit()
        conn.close()
    
    # ========== DIARY OPERATIONS ==========
    
    def create_diary_entry(self, entry_date: str, title: str, content: str, 
                          mood: str = "neutral", tags: List[str] = None) -> int:
        """Create a diary entry"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        tags = tags or []
        cursor.execute("""
            INSERT INTO diary_entries (entry_date, title, content, mood, tags)
            VALUES (?, ?, ?, ?, ?)
        """, (entry_date, title, content, mood, json.dumps(tags)))
        
        entry_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return entry_id
    
    def get_diary_entry(self, entry_date: str) -> Optional[Dict]:
        """Get diary entry for a specific date"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM diary_entries WHERE entry_date = ?", (entry_date,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            entry = dict(row)
            entry['tags'] = json.loads(entry.get('tags', '[]'))
            return entry
        return None
    
    def get_all_diary_entries(self) -> List[Dict]:
        """Get all diary entries"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM diary_entries ORDER BY entry_date DESC")
        entries = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        for entry in entries:
            entry['tags'] = json.loads(entry.get('tags', '[]'))
        
        return entries
    
    def update_diary_entry(self, entry_date: str, title: str = None, content: str = None, 
                          mood: str = None, tags: List[str] = None):
        """Update a diary entry"""
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
        if mood is not None:
            updates.append("mood = ?")
            params.append(mood)
        if tags is not None:
            updates.append("tags = ?")
            params.append(json.dumps(tags))
        
        if updates:
            updates.append("updated_at = CURRENT_TIMESTAMP")
            query = f"UPDATE diary_entries SET {', '.join(updates)} WHERE entry_date = ?"
            params.append(entry_date)
            cursor.execute(query, params)
            conn.commit()
        
        conn.close()
    
    def delete_diary_entry(self, entry_date: str):
        """Delete a diary entry"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM diary_entries WHERE entry_date = ?", (entry_date,))
        conn.commit()
        conn.close()
    
    # ========== PREFERENCES ==========
    
    def get_preferences(self) -> Dict:
        """Get user preferences"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM preferences LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        else:
            # Create default preferences
            self.set_preferences()
            return self.get_preferences()
    
    def set_preferences(self, theme: str = "light", accent_color: str = "#6366f1", 
                       font_size: int = 16, auto_save: int = 1):
        """Set user preferences"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if preferences exist
        cursor.execute("SELECT id FROM preferences LIMIT 1")
        exists = cursor.fetchone()
        
        if exists:
            cursor.execute("""
                UPDATE preferences 
                SET theme = ?, accent_color = ?, font_size = ?, auto_save = ?
            """, (theme, accent_color, font_size, auto_save))
        else:
            cursor.execute("""
                INSERT INTO preferences (theme, accent_color, font_size, auto_save)
                VALUES (?, ?, ?, ?)
            """, (theme, accent_color, font_size, auto_save))
        
        conn.commit()
        conn.close()

# Initialize database on import
db = NotesDatabase()