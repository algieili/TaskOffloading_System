from fastapi import FastAPI
from supabase_client import supabase
app = FastAPI()

@app.get("/")
@app.head("/")
def home():
    return {"status": "ok"}
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
// render
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "ok"}

@app.get("/test")
def test():
    return {
        "message": "Render + Vercel connection working 🚀",
        "success": True
    }
