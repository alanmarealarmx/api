from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserInput(BaseModel):
    text: str

@app.post("/capture_input")
def capture_input(user_input: UserInput):
    return {"received_text": user_input.text}

@app.get("/")
def read_root():
    return {"message": "API está funcionando corretamente!"}
