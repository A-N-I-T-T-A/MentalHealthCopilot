# utils/db.py
import sqlite3
from datetime import datetime
import hashlib

DB_PATH = "mental_health.db"

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    """Initialize all required tables."""
    conn = get_connection()
    c = conn.cursor()

    # Users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password_hash TEXT,
            created_at TIMESTAMP
        )
    """)

    # Journal entries table
    c.execute("""
        CREATE TABLE IF NOT EXISTS journal_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            entry TEXT,
            emotion TEXT,
            confidence REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user) REFERENCES users(email)
        )
    """)

    conn.commit()
    conn.close()

# ------------------------
# AUTHENTICATION HELPERS
# ------------------------

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(email, password):
    """Register a new user (with hashed password)."""
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (email, password_hash, created_at) VALUES (?, ?, ?)",
                  (email, hash_password(password), datetime.now()))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(email, password):
    """Check credentials against DB."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=? AND password_hash=?",
              (email, hash_password(password)))
    user = c.fetchone()
    conn.close()
    return user

# ------------------------
# JOURNAL ENTRY HELPERS
# ------------------------

def add_entry(user, entry, emotion, confidence):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO journal_entries (user, entry, emotion, confidence, timestamp) VALUES (?, ?, ?, ?, ?)",
              (user, entry, emotion, confidence, datetime.now()))
    conn.commit()
    conn.close()

def get_entries(user):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM journal_entries WHERE user=?", (user,))
    rows = c.fetchall()
    conn.close()
    return rows

def delete_entry(entry_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM journal_entries WHERE id=?", (entry_id,))
    conn.commit()
    conn.close()

def get_entries_grouped_by_date(user):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT DATE(timestamp) as date, emotion, COUNT(*) as count 
        FROM journal_entries 
        WHERE user=?
        GROUP BY date, emotion
    """, (user,))
    results = c.fetchall()
    conn.close()
    return results

def create_checkins_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS checkins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            response TEXT,
            timestamp TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def add_checkin(user, response):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO checkins (user, response, timestamp) VALUES (?, ?, ?)
    """, (user, response, datetime.now()))
    conn.commit()
    conn.close()

def create_preferences_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS preferences (
            user TEXT PRIMARY KEY,
            tone TEXT
        )
    """)
    conn.commit()
    conn.close()

def set_user_tone(user, tone):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO preferences (user, tone) VALUES (?, ?)", (user, tone))
    conn.commit()
    conn.close()

def get_user_tone(user):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT tone FROM preferences WHERE user = ?", (user,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else "neutral"
def get_last_entry(user):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT entry, emotion FROM journal_entries
        WHERE user = ?
        ORDER BY timestamp DESC
        LIMIT 1
    """, (user,))
    result = c.fetchone()
    conn.close()
    return result if result else ("", "")

# ------------------------
# ADMIN FUNCTIONALITY
# ------------------------

def create_admins_table():
    """Create admins table for admin authentication."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password_hash TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def register_admin(email, password):
    """Register a new admin."""
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO admins (email, password_hash) VALUES (?, ?)",
                  (email, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_admin(email, password):
    """Check admin credentials."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM admins WHERE email=? AND password_hash=?",
              (email, hash_password(password)))
    admin = c.fetchone()
    conn.close()
    return admin

def get_all_users():
    """Get all registered users."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT email, created_at FROM users ORDER BY created_at DESC")
    users = c.fetchall()
    conn.close()
    return users

def get_all_entries():
    """Get all journal entries (without sensitive content)."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT user, emotion, confidence, timestamp 
        FROM journal_entries 
        ORDER BY timestamp DESC
    """)
    entries = c.fetchall()
    conn.close()
    return entries

def get_active_users(days=7):
    """Get users who have written journal entries in the last N days."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT DISTINCT user 
        FROM journal_entries 
        WHERE timestamp >= datetime('now', '-{} days')
    """.format(days))
    active_users = c.fetchall()
    conn.close()
    return [user[0] for user in active_users]

def get_user_registrations_by_month():
    """Get user registrations grouped by month."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT strftime('%Y-%m', created_at) as month, COUNT(*) as count
        FROM users 
        GROUP BY strftime('%Y-%m', created_at)
        ORDER BY month
    """)
    registrations = c.fetchall()
    conn.close()
    return registrations

def get_journal_activity_by_day():
    """Get journal entries grouped by day."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT DATE(timestamp) as date, COUNT(*) as count
        FROM journal_entries 
        GROUP BY DATE(timestamp)
        ORDER BY date
    """)
    activity = c.fetchall()
    conn.close()
    return activity

def get_emotion_distribution():
    """Get emotion distribution across all entries."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT emotion, COUNT(*) as count
        FROM journal_entries 
        GROUP BY emotion
        ORDER BY count DESC
    """)
    emotions = c.fetchall()
    conn.close()
    return emotions

def get_emotion_trends_by_week():
    """Get emotion trends grouped by week."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT strftime('%Y-%W', timestamp) as week, emotion, COUNT(*) as count
        FROM journal_entries 
        GROUP BY strftime('%Y-%W', timestamp), emotion
        ORDER BY week
    """)
    trends = c.fetchall()
    conn.close()
    return trends

def delete_user_and_entries(user_email):
    """Delete a user and all their journal entries."""
    conn = get_connection()
    c = conn.cursor()
    try:
        # Delete journal entries first (foreign key constraint)
        c.execute("DELETE FROM journal_entries WHERE user = ?", (user_email,))
        # Delete user
        c.execute("DELETE FROM users WHERE email = ?", (user_email,))
        # Delete preferences
        c.execute("DELETE FROM preferences WHERE user = ?", (user_email,))
        # Delete checkins
        c.execute("DELETE FROM checkins WHERE user = ?", (user_email,))
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        return False
    finally:
        conn.close()

def get_database_size():
    """Get database file size in MB."""
    try:
        import os
        size_bytes = os.path.getsize(DB_PATH)
        size_mb = size_bytes / (1024 * 1024)
        return round(size_mb, 2)
    except Exception:
        return 0

def change_user_password(email, current_password, new_password):
    """Change user password after verifying current password."""
    conn = get_connection()
    c = conn.cursor()
    try:
        # First verify the current password
        c.execute("SELECT * FROM users WHERE email=? AND password_hash=?", 
                  (email, hash_password(current_password)))
        user = c.fetchone()
        
        if not user:
            return False, "Current password is incorrect"
        
        # Update the password
        c.execute("UPDATE users SET password_hash=? WHERE email=?", 
                  (hash_password(new_password), email))
        conn.commit()
        return True, "Password updated successfully"
    except Exception as e:
        return False, f"Error updating password: {str(e)}"
    finally:
        conn.close()