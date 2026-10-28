## Technologies

- Python
- FastAPI
- Pydantic
- Requests
- python-dotenv
- Uvicorn

## Requirements

- Python 3.12 or compatible version
- An API key for a supported AI service

## Installation

Clone the repository:

```bash
git clone https://github.com/Pouran-ai/ai-streaming-chat-api.git
cd ai-streaming-chat-api

Create and activate a virtual environment:
python -m venv venv
.\venv\Scripts\Activate.ps1

Install dependencies:
python -m pip install -r requirements.txt

Configuration
Create a file named key.env in the project directory:
AVALAI_API_KEY=your_api_key_here

Replace the placeholder with your own API key.
Never publish your API key or commit key.env.
Running the API
Start the development server:
python -m uvicorn test:app --reload

Open the API documentation:

http://127.0.0.1:8000/docs
Chat Endpoint
POST /chat

Example request:
{
  "message": "Hello!"
}

Example response:
{
  "reply": "Hello! How can I help you?",
  "status": "success"
}

The actual reply depends on the configured AI service.
## Current Limitations
- Conversation history is stored in memory.
- Conversation history is lost when the server restarts.
- This project is intended for learning and is not yet production-ready.
## License
No license has been selected yet.