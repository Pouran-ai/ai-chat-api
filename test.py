
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field
import requests
import sqlite3


app = FastAPI(
    title="AI Chat API",
    description="Chat API powered by local Ollama and Qwen",
    version="2.0.0"
)

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen2.5:3b"
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


init_db()

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
class PromptRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    user_id:str = Field(min_length=1,max_length=100)
    message: str = Field(min_length=1, max_length=1000)

@app.post("/chat")
def chat_with_ai(request: PromptRequest):
    user_id = request.user_id

    user_history = get_chat_history(user_id)
    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ] + user_history + [
        {"role": "user", "content": request.message}
    ]

    data = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=data,
            timeout=120)

        response.raise_for_status()

        result = response.json()
        answer = result["message"]["content"]
        save_message(user_id, "user", request.message)
        save_message(user_id, "assistant", answer)
        return {
            "reply": answer,
            "status": "success"
        }

    except requests.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Cannot connect to Ollama. Make sure Ollama is running."
        )

    except requests.Timeout:
        raise HTTPException(
            status_code=504,
            detail="Ollama response timed out."
        )

    except requests.RequestException:
        raise HTTPException(
            status_code=502,
            detail="Error communicating with Ollama."
        )

    except (ValueError, KeyError, TypeError):
        raise HTTPException(
            status_code=502,
            detail="Invalid response received from Ollama."
        )
@app.delete("/chat/{user_id}")
def delete_chat_history(user_id: str):
    try:
        conn = sqlite3.connect(DB_NAME)

        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM messages WHERE user_id = ?",
            (user_id,)
        )

        deleted_count = cursor.rowcount

        conn.commit()

    except sqlite3.Error:
        raise HTTPException(
            status_code=500,
            detail="Database error while deleting chat history."
        )

    finally:
        if "conn" in locals():
            conn.close()

    if deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="User history not found."
        )

    return {
        "message": "Chat history deleted successfully.",
        "status": "success"
    }