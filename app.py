from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field

class stu(BaseModel):
    id:int
    name:str
    math:float = Field(ge=0,le=100)
    science:float = Field(ge=0,le=100)
    english:float = Field(ge=0,le=100)

class stu_up(BaseModel):
    name:str|None = None
    math:float|None = Field(default=None,ge=0,le=100)
    science:float|None = Field(default=None,ge=0,le=100)
    english:float|None = Field(default=None,ge=0,le=100)
    
app = FastAPI()
students = {}

@app.get("/students")
def get_stu():
    return list(students.values())

@app.post("/students")
def post_stu(s:stu):
    if s.id in students:
        raise HTTPException(400,"Student exists already")
    else:
        students[s.id] = s

@app.get("/students/{sid}")
def get_stu_id(sid:int):
    if sid not in students:
        raise HTTPException(404,"Not found")
    else:
        return students[sid]

@app.patch("/students/{sid}")
def patch_stu_id(sid:int,s:stu_up):
    if sid not in students:
        raise HTTPException(404,"Not found")
    else:
        students[sid] = students[sid].model_copy(update = s.model_dump(exclude_unset=True))
        return students[sid]

@app.delete("/students/{sid}")
def del_stu_id(sid:int):
    if sid not in students:
        raise HTTPException(404,"Not found")
    else:
        del students[sid]
        return {"message":"Done"}