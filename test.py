from fastapi import FastAPI,HTTPException
from pydantic import BaseModel, ConfigDict, Field
from dotenv import load_dotenv
import requests
import os
app=FastAPI()
load_dotenv("key.env")
API_KEY = os.getenv("AVALAI_API_KEY")

chat_history=[]
class PromptRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    message: str = Field(min_length=1, max_length=1000 )
@app.post('/chat')
def chat_with_ai(request:PromptRequest):
    if not API_KEY:
        raise HTTPException(
        status_code=500,
        detail="API key is not configured"
    )
    headers={
    "Authorization":f"Bearer {API_KEY}","Content-Type":"application/json"
    }
    data={
        "model":"gpt-5.6-luna",
        "messages":[
        {
        "role":"system",
        "content":"you are a helpful assistant."
        }
        ] + chat_history + [{"role": "user","content": request.message}]}
    try:
     res=requests.post(
         "https://api.avalai.ir/v1/chat/completions",
         headers=headers,
         json= data,
         timeout=60)
     res.raise_for_status()
     result=res.json()
     answer=result["choices"][0]["message"]["content"]
     chat_history.append({
    "role": "user",
    "content": request.message
     })
     chat_history.append({
        "role":"assistant",
        "content":answer
        })
     return {"reply":answer,"status":"success" }
    except requests.RequestException:
        raise HTTPException(status_code = 502,detail="Error connecting to the AIservice")
    except (ValueError, KeyError, IndexError, TypeError):
        raise HTTPException(status_code=502,detail="Invalid response received from the AIservice")