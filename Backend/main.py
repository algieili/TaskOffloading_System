from fastapi import FastAPI

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
