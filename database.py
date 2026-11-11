import sqlite3
from fastapi import HTTPException
DB_NAME = "chat_history.db"
def init_db():
    conn = sqlite3.connect(DB_NAME)

    try:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL
        )
        """)

        conn.commit()

    finally:
        conn.close()
def get_chat_history(user_id: str):
    try:
        conn = sqlite3.connect(DB_NAME)

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT role, content
            FROM messages
            WHERE user_id = ?
            ORDER BY id
            """,
            (user_id,)
        )

        rows = cursor.fetchall()

        return [
            {"role": role, "content": content}
            for role, content in rows
        ]

    except sqlite3.Error:
        raise HTTPException(
            status_code=500,
            detail="Database error while retrieving chat history."
        )

    finally:
        if "conn" in locals():
            conn.close()
def save_message(user_id: str, role: str, content: str):
    try:
        conn = sqlite3.connect(DB_NAME)

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO messages (user_id, role, content)
            VALUES (?, ?, ?)
            """,
            (user_id, role, content)
        )

        conn.commit()

    except sqlite3.Error:
        raise HTTPException(
            status_code=500,
            detail="Database error while saving message."
        )

    finally:
        if "conn" in locals():
            conn.close()
def delete_user_history(user_id: str):
    try:
        conn = sqlite3.connect(DB_NAME)

        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM messages WHERE user_id = ?",
            (user_id,)
        )

        deleted_count = cursor.rowcount

        conn.commit()

        return deleted_count

    except sqlite3.Error:
        raise HTTPException(
            status_code=500,
            detail="Database error while deleting chat history."
        )

    finally:
        if "conn" in locals():
            conn.close()