from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import random

app = FastAPI()

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load CSV on startup
wines_df = pd.read_csv("wines_data.csv")

def recommend_wine(wine_type=None):
    df = wines_df
    if wine_type:
        df = df[df['Type'].str.lower() == wine_type.lower()]
    if df.empty:
        return "Sorry, I couldn't find any wine matching your request."
    wine = df.sample(1).iloc[0]
    return (
        f"I recommend {wine['WineName']} ({wine['Type']}, {wine['Country']}). "
        f"ABV: {wine['ABV']}%, Body: {wine['Body']}, Acidity: {wine['Acidity']}. "
        f"Find more: {wine['Website']}"
    )

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "")
    # Very basic intent detection: look for wine type keywords
    wine_type = None
    for t in ["red", "white", "rosé", "sparkling"]:
        if t in user_message.lower():
            wine_type = t
            break
    response = recommend_wine(wine_type)
    return {"response": response}