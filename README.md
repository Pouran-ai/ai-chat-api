# AI Streaming Chat API
A FastAPI-based backend that connects to Language Models (LLMs) via AvalAI, featuring real-time streaming responses.

## 
- Real-time streaming: Responses appear word-by-word (like ChatGPT).
- conversation Memory: Keeps track of the chat history.
- Custom system Prompts: Define the AI's personality.
- Simple Frontend: Includes an HTML/JS page for testing.

  ## Tech Stack
  - Python
  - FastAPI
  - Pydantic
  - HTML / javaScript
  - AvalAI (LLM Provider)
 
    ## How to Run
    1. Instll dependencies:
    pip install fastapi uvicorn requests
    2. Run the server:
    uvicorn main: --reload
    3. Open the frontend in your browser:
    http://127.0.0.1.8000/index.html
    
