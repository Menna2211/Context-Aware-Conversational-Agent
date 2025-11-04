import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uvicorn
from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents import build_context_aware_agent
from langchain_core.messages import HumanMessage

# ============================================
# AGENT INITIALIZATION
# ============================================

agent = build_context_aware_agent()

# ============================================
# FASTAPI SETUP
# ============================================

app = FastAPI(
    title="Context-Aware AI Chatbot",
    description="Stateless chatbot - No memory saved between messages",
    version="1.0.0"
)

# CORS for frontend apps (React/Next.js/Flutter/etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# REQUEST MODELS
# ============================================

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

# ============================================
# CHAT ENDPOINT - FIXED VERSION
# ============================================

from fastapi import Request
import json

@app.post("/chat")
async def chat(request: Request):
    try:
        # Parse JSON manually
        body = await request.json()
        message = body.get("message", "").strip()
        if not message:
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        result = agent.invoke({"messages": [HumanMessage(content=message)]})
        answer = result["messages"][-1].content
        
        return {"response": answer}
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")

# ============================================
# ROOT ENDPOINT
# ============================================

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Stateless Chatbot API running!"}

# ============================================
# RUN SERVER
# ============================================

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)