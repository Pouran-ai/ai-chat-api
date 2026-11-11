
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from model_service import call_model
from database import (
    init_db,
    get_chat_history,
    save_message,
    delete_user_history
)
import requests

app = FastAPI(
    title="AI Chat API",
    description="Chat API powered by local Ollama and Qwen",
    version="2.0.0"
)
init_db()
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
    try:
        answer = call_model(messages)
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
    except (ValueError, KeyError, TypeError):
      raise HTTPException(
        status_code=502,
        detail="Invalid response received from Ollama."
      )

    except requests.RequestException:
      raise HTTPException(
        status_code=502,
        detail="Error communicating with Ollama."
      )
@app.delete("/chat/{user_id}")
def delete_chat_history(user_id: str):

    deleted_count = delete_user_history(user_id)

    if deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="User history not found."
        )

    return {
        "message": "Chat history deleted successfully.",
        "status": "success"
    }