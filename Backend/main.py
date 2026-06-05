from fastapi import FastAPI
from supabase_client import supabase

app = FastAPI()

@app.get("/")
def home():
    return {"status": "ok"}
