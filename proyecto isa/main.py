from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
import os

app = FastAPI()

# Servir archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Plantillas HTML
templates = Jinja2Templates(directory="templates")

# Cargar o crear archivo de ventas
file_name = "BELLEZA_PURA_LISTA_PARA_CARGAR (1).xlsx"
if os.path.exists(file_name):
    df = pd.read_excel(file_name)
else:
    df = pd.DataFrame(columns=["cliente", "categoria", "cantidad", "marca", "precio"])

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/registrar_venta", response_class=HTMLResponse)
async def registrar_venta(
    request: Request,
    cliente: str = Form(...),
    categoria: str = Form(...),
    cantidad: int = Form(...),
    marca: str = Form(...),
    precio: float = Form(...)
):
    global df
    nueva_venta = {
        "cliente": cliente,
        "categoria": categoria,
        "cantidad": cantidad,
        "marca": marca,
        "precio": precio
    }
    df = pd.concat([df, pd.DataFrame([nueva_venta])], ignore_index=True)
    df.to_excel(file_name, index=False)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "mensaje": "✅ Venta registrada con éxito!"
    })

@app.get("/reportes", response_class=HTMLResponse)
async def reportes(request: Request):
    return templates.TemplateResponse("reportes.html", {"request": request})