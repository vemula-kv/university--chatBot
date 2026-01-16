import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import json
from rag_service import RagService

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

# Mount frontend directory for static assets (css, js)
# Use absolute path to be safe regardless of where python is run from
current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(current_dir, "../frontend")

app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

# Enable CORS (still good to have)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(frontend_dir, "index.html"))

# Initialize RAG Service
rag = RagService()

class ChatRequest(BaseModel):
    message: str
    context: Optional[str] = None

@app.get("/init")
async def get_initial_buttons():
    """Returns the main menu buttons."""
    return {
        "buttons": [
            {"label": "Academic Programs", "value": "academic_programs", "type": "category"},
            {"label": "Admissions", "value": "admissions", "type": "category"},
            {"label": "Tuition & Fees", "value": "tuition", "type": "category"},
            {"label": "Campus Life & Housing", "value": "campus_life", "type": "category"},
            {"label": "Ask a Question", "value": "ask_ai", "type": "mode_switch"}
        ]
    }

@app.post("/chat")
async def chat(request: ChatRequest):
    """Handles logic for both button clicks and AI queries."""
    
    msg = request.message.lower()
    
    # 1. Handle Categorical Button Clicks (Navigation)
    if msg == "academic_programs":
        return {
            "text": "Explore our wide range of academic offerings.",
            "buttons": [
                {"label": "Science & Biology", "value": "courses_biology", "type": "query"},
                {"label": "Data Science Programs", "value": "courses_data_science", "type": "query"},
                {"label": "Show All Majors", "value": "courses_general", "type": "query"},
                {"label": "⬅ Back", "value": "init", "type": "category"}
            ]
        }
    
    elif msg == "admissions":
        return {
            "text": "Find out how to join our community.",
            "buttons": [
                {"label": "How to Apply", "value": "admissions_undergraduate", "type": "query"},
                {"label": "International Students", "value": "admissions_international", "type": "query"},
                {"label": "Transfer Info", "value": "admissions_transfer", "type": "query"},
                {"label": "⬅ Back", "value": "init", "type": "category"}
            ]
        }
        
    elif msg == "tuition":
        return {
            "text": "Everything you need to know about costs and aid.",
            "buttons": [
                {"label": "In-State Tuition", "value": "fees_tuition_in_state", "type": "query"},
                {"label": "Out-of-State Tuition", "value": "fees_tuition_out_of_state", "type": "query"},
                {"label": "Scholarships", "value": "fees_scholarships", "type": "query"},
                {"label": "⬅ Back", "value": "init", "type": "category"}
            ]
        }

    elif msg == "campus_life":
        return {
            "text": "Discover life on campus.",
            "buttons": [
                {"label": "Housing Options", "value": "campus_life_housing", "type": "query"},
                {"label": "Sports Programs", "value": "campus_life_sports", "type": "query"},
                {"label": "Mental Health Support", "value": "campus_life_mental_health", "type": "query"},
                {"label": "⬅ Back", "value": "init", "type": "category"}
            ]
        }

    elif msg == "init":
        return await get_initial_buttons()
    
    # 2. Handle Specific Queries (either from sub-buttons or type-in)
    # If the message matches a key in our mock data structure (underscore separated)
    # we can try to find it directly, OR we just pass it to the AI RAG service
    
    response_text = rag.get_response(msg)
    
    return {
        "text": response_text,
        "buttons": [
           {"label": "Ask Another Question", "value": "ask_ai", "type": "mode_switch"},
           {"label": "Main Menu", "value": "init", "type": "category"}
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
