from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from fastapi.responses import HTMLResponse

import json
import requests
app=FastAPI()
chat_history = []
@app.get("/")
def read_boot():
    return {"message": "Hello. This is my first API"}
class User(BaseModel):
    name: str
    age: int
@app.post("/users")
def create_user(user:User):
    return {
        "message": f"hello {user.name}! you {user.age} years old" ,
        "status": "success"
    }
class PromptRequest(BaseModel):
    message: str
@app.post("/chat")
def chat_with_ai(request: PromptRequest):
    chat_history.append({"role":"user" , "content":request.message})
    headers = { 
               "Authorization": "YOUR_API_KEY_HERE",
               "Content-Type": "aplication/json"
    }
    
    data ={
        "model": "gpt-5.6-luna",
        "messages": [{"role":"system" , "content":"to yek dastyar hasti"}] + chat_history,
        "stream":True
    }
    
    def generate():
      try:
        res = requests.post("https://api.avalai.ir/v1/chat/completions", headers=headers,json=data,stream=True)
        for line in res.iter_lines():
            if line:
                line_text = line.decode("utf-8")
                if line_text.startswith("data: "):
                    data_str = line_text[6:]
                    if data_str != '[DONE]':
                        try:
                            json_data = json.loads(data_str)
                            chunk = json_data["choices"][0]['delta'].get("content",'')
                            if chunk:
                                yield chunk
                        except:
                            pass
      except Exception as e:
        yield f"Error:{str(e)}"
    return StreamingResponse(generate(),media_type="text/plain")
@app.get("/index.html", response_class=HTMLResponse)
def read_index():
    with open("index.html" , "r", encoding="utf-8") as f:
       return f.read()

        
    