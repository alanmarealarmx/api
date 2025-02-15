import os
import json
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel

app = FastAPI()

# 🔹 Carregar credenciais do Google Sheets a partir das variáveis de ambiente
try:
    creds_json = json.loads(os.getenv("GOOGLE_CREDENTIALS"))
except Exception as e:
    print(f"❌ Erro ao carregar GOOGLE_CREDENTIALS: {e}")
    raise ValueError("Variável de ambiente GOOGLE_CREDENTIALS não encontrada ou inválida.")

# 🔹 Configurar a autenticação no Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
client = gspread.authorize(creds)

# 🔹 ID da planilha do Google Sheets (Substitua pelo ID correto)
SHEET_ID = "SEU_ID_DA_PLANILHA"

# 🔹 Verificar se a planilha existe e pode ser acessada
try:
    sheet = client.open_by_key(SHEET_ID).sheet1
    sheet.append_row(["Teste de conexão bem-sucedido!"])
    print("✅ Conexão com Google Sheets funcionando corretamente.")
except gspread.exceptions.SpreadsheetNotFound:
    print(f"❌ Erro: Planilha com ID {SHEET_ID} não encontrada.")
    print("📌 Verifique se o ID está correto e se a conta de serviço tem acesso como Editor.")
    raise
except Exception as e:
    print(f"❌ Erro inesperado ao acessar Google Sheets: {e}")
    raise

class UserInput(BaseModel):
    text: str

def save_to_google_sheets(text: str):
    """Salva os dados no Google Sheets com delay e tentativas automáticas"""
    time.sleep(2)  # 🔹 Aguarda 2 segundos para evitar sobrecarga no Google Sheets

    for attempt in range(3):  # 🔹 Tenta 3 vezes antes de desistir
        try:
            sheet.append_row([text])
            print(f"✅ Dado salvo na planilha: {text}")
            return
        except Exception as e:
            print(f"⚠️ Erro ao salvar no Google Sheets (Tentativa {attempt+1}): {e}")
            time.sleep(5)  # 🔹 Aguarda 5 segundos antes de tentar de novo

    print("❌ Falha ao salvar no Google Sheets após 3 tentativas.")

@app.post("/capture_input")
def capture_input(user_input: UserInput, background_tasks: BackgroundTasks):
    """Captura o que o usuário digitou e salva no Google Sheets"""
    background_tasks.add_task(save_to_google_sheets, user_input.text)
    return {"message": "Entrada capturada com sucesso!"}

@app.get("/")
def read_root():
    return {"message": "API está funcionando corretamente!"}
