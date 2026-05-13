# app/main.py
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# IMPORTAÇÃO DOS ROUTERS: Como a pasta backend está dentro de app
from app.backend.FastAPI.routers import locais as locais

app = FastAPI(title="VeritasIA - Módulos Front-end e Back-end")

# 1. Localiza dinamicamente a pasta 'app/' onde este main.py está rodando
APP_DIR = Path(__file__).resolve().parent

# 2. Configura o caminho para 'app/frontend/static'
STATIC_DIR = APP_DIR / "app" / "frontend" / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# 3. Configura o caminho para 'app/frontend/templates'
TEMPLATES_DIR = APP_DIR / "app" / "frontend" / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# 4. Inclui as rotas do Back-end
app.include_router(locais.router)


# ================= ROTAS DE VIEW (HTML) =================

@app.get("/teste", response_class=HTMLResponse, tags=["Views"])
async def pagina_inicial(request: Request):
    contexto = {
        "request": request, 
        "titulo": "Dashboard VeritasIA",
        "descricao": "Monitoramento de Notícias sobre Feminicídio"
    }
    return templates.TemplateResponse(request=request, name="index.html", context=contexto)