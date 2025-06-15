from fastapi import FastAPI,UploadFile, Form, File
from fastapi.middleware.cors import CORSMiddleware
import json
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://search-debouncing-1.onrender.com"],  # Replace "*" with specific frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/notes')
def home():
    return {"message":"Hello,swastik"}


@app.get("/stations/search")
def search_notes(q:str=""):
    with open("trainData.json","r",encoding="utf-8") as f:
        data=json.load(f)
    filtered = [
            {"code":s["code"],"station":s["Country"]}
            for s in data["data"]
            if q.lower() in s["Country"].lower() or q.lower() in s["code"].lower()
            ]
    return filtered



