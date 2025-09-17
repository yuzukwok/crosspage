from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv
from crossword_generator import generate_crossword
from llm_definition import batch_generate_definitions
from crossword_html import generate_crossword_html
import tempfile

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

class GenerateHTMLRequest(BaseModel):
    grid: List[List[str]]
    layout: List[Dict]
    clues: Dict[str, str]
    style: Optional[str] = 'classic'

@app.post("/api/crossword")
async def api_crossword(req: GenerateRequest):
    words = req.words
    grid, layout = generate_crossword(words, req.size)
    clues: Dict[str, str] = {}
    if req.use_llm:
        try:
            clues = batch_generate_definitions(words)
        except Exception as e:
            # 如果LLM失败，使用单词本身作为提示
            clues = {w: f"What is '{w}'?" for w in words}
    else:
        clues = {w: f"What is '{w}'?" for w in words}
    return {"grid": grid, "layout": layout, "clues": clues}

@app.post("/api/generate-html")
async def api_generate_html(req: GenerateHTMLRequest):
    """生成并返回HTML文件"""
    try:
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            temp_file = f.name
        
        # 生成HTML
        generate_crossword_html(req.grid, req.layout, req.clues, temp_file, req.style)
        
        # 读取HTML内容
        with open(temp_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 清理临时文件
        os.unlink(temp_file)
        
        # 返回HTML内容
        return Response(
            content=html_content,
            media_type="text/html",
            headers={
                "Content-Disposition": f'attachment; filename="crossword-{req.style}.html"'
            }
        )
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
