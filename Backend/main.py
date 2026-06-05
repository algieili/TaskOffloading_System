from fastapi import FastAPI
from supabase_client import supabase

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Backend running"}

@app.get("/tasks")
def get_tasks():
    return supabase.table("tasks").select("*").execute().data
