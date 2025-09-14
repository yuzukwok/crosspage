from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv
from crossword_generator import generate_crossword
from llm_definition import batch_generate_definitions

load_dotenv()

app = FastAPI(title="Crossword API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    words: List[str]
    size: Optional[int] = 12
    use_llm: Optional[bool] = True

@app.post("/api/crossword")
async def api_crossword(req: GenerateRequest):
    words = req.words
    grid, layout = generate_crossword(words, req.size)
    clues: Dict[str, str] = {}
    if req.use_llm:
        clues = batch_generate_definitions(words)
    else:
        clues = {w: w for w in words}
    return {"grid": grid, "layout": layout, "clues": clues}

@app.get("/api/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
