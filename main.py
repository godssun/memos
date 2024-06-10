from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional

class Memo(BaseModel):
    id: int
    content: str
    title: Optional[str] = None
    createAt: Optional[str] = None

memos = []

app = FastAPI()

@app.post("/memos")
def create_memo(memo: Memo):
    memos.append(memo.dict())
    return {'message': '메모 추가 성공'}

@app.get("/memos")
def read_memo(sortedBy: str = Query('createAt', regex="^(content|title|createAt)$"), order: str = Query('ASC', regex="^(ASC|DESC)$")):
    def get_key(memo):
        value = memo.get(sortedBy)
        return value if value is not None else ""
    
    sorted_memos = sorted(memos, key=get_key, reverse=(order == 'DESC'))
    return sorted_memos

@app.put("/memos/{memo_id}")
def put_memo(memo_id: int, req_memo: Memo):
    for memo in memos:
        if memo['id'] == memo_id:
            memo['content'] = req_memo.content
            if req_memo.title is not None:
                memo['title'] = req_memo.title
            if req_memo.createAt is not None:
                memo['createAt'] = req_memo.createAt
            return {'message': '성공'}
    raise HTTPException(status_code=404, detail="그런 메모 없음")

@app.delete("/memos/{memo_id}")
def delete_memo(memo_id: int):
    for index, memo in enumerate(memos):
        if memo['id'] == memo_id:
            memos.pop(index)
            return {'message': '성공'}
    raise HTTPException(status_code=404, detail="그런 메모 없음")

app.mount("/", StaticFiles(directory='static', html=True), name='static')
