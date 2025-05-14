from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import uvicorn
from datetime import datetime
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="public"), name="static")

# Templates
templates = Jinja2Templates(directory=".")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    with open("index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.post("/signup")
async def signup(
    name: str = Form(...),
    email: str = Form(...),
    company: str = Form(...),
    role: str = Form(...)
):
    try:
        # Format the signup data
        signup_data = {
            "name": name,
            "email": email,
            "company": company,
            "role": role
        }
        
        # Insert into Supabase
        result = supabase.table("signups").insert(signup_data).execute()
        
        return JSONResponse({
            "status": "success",
            "message": "Thank you for your interest! We will contact you soon."
        })
    except Exception as e:
        return JSONResponse({
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }, status_code=500)

@app.get("/signups")
async def get_signups():
    try:
        # Fetch all signups from Supabase
        result = supabase.table("signups").select("*").execute()
        
        return JSONResponse({
            "status": "success",
            "signups": result.data
        })
    except Exception as e:
        return JSONResponse({
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }, status_code=500)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 