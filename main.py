from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

class Memo(BaseModel):
    id: int
    content: str

memos = []

app = FastAPI()

@app.post("/memos")
def create_memo(memo: Memo):
    memos.append(memo)
    return {'message': '메모 추가 성공'}

@app.get("/memos")
def read_memo():
    return memos

@app.put("/memos/{memo_id}")
def put_memo(memo_id: int, req_memo: Memo):
    for memo in memos:
        if memo.id == memo_id:
            memo.content = req_memo.content
            return {'message': '성공'}
    raise HTTPException(status_code=404, detail="그런 메모 없음")

@app.delete("/memos/{memo_id}")
def delete_memo(memo_id: int):
    for index, memo in enumerate(memos):
        if memo.id == memo_id:
            memos.pop(index)
            return {'message': '성공'}
    raise HTTPException(status_code=404, detail="그런 메모 없음")

app.mount("/", StaticFiles(directory='static', html=True), name='static')

