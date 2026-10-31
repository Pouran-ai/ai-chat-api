
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field
import requests

app = FastAPI(
    title="AI Chat API",
    description="Chat API powered by local Ollama and Qwen",
    version="2.0.0"
)

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen2.5:3b"

chat_history = []


class PromptRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    message: str = Field(min_length=1, max_length=1000)


@app.post("/chat")
def chat_with_ai(request: PromptRequest):

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        }
    ] + chat_history + [
        {
            "role": "user",
            "content": request.message
        }
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
            timeout=120
        )

        response.raise_for_status()

        result = response.json()

        answer = result["message"]["content"]

        chat_history.append({
            "role": "user",
            "content": request.message
        })

        chat_history.append({
            "role": "assistant",
            "content": answer
        })

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
