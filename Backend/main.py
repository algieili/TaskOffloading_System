from fastapi import FastAPI

app = FastAPI()

@app.get("/")
@app.head("/")
def home():
    return {"status": "ok"}
