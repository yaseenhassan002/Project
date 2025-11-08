from fastapi import FastAPI
import uvicorn
import transformers
import nest_asyncio

app = FastAPI()

@app.get("/welcome")
def welcome():
    return {"message": "Hello World"}

