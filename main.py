import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel

app = FastAPI()

# 🔹 Ler credenciais do Render (variável de ambiente)
creds_json = json.loads(os.getenv("GOOGLE_CREDENTIALS"))

# 🔹 Configurar a API do Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
client = gspread.authorize(creds)

# 🔹 ID da sua planilha no Google Sheets (mude para o seu ID)
SHEET_ID = "1_zA1A3ts1chz9HkqOvFxA3ql9fcN9s4JD_hf-6aKRRE"
sheet = client.open_by_key(SHEET_ID).sheet1

class UserInput(BaseModel):
    text: str

def save_to_google_sheets(text: str):
    """Salva os dados no Google Sheets"""
    sheet.append_row([text])
    print(f"🔹 Dado salvo na planilha: {text}")

@app.post("/capture_input")
def capture_input(user_input: UserInput, background_tasks: BackgroundTasks):
    """Captura o que o usuário digitou e salva no Google Sheets"""
    background_tasks.add_task(save_to_google_sheets, user_input.text)
    return {}

@app.get("/")
def read_root():
    return {"message": "API está funcionando corretamente!"}
