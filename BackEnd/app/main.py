
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# IMPORTAÇÃO DOS ROUTERS: Como a pasta backend está dentro de app
from FastAPI.routers import locais as locais
app = FastAPI(title="VeritasIA - Módulos Front-end e Back-end")

# backend/app/main.py
# backend/app/main.py
app.mount("/static", StaticFiles(directory="../../FrontEnd/app/static"), name="static")

# 3. Configura o caminho para 'app/frontend/templates'

templates = Jinja2Templates(directory="../../FrontEnd/app/templates")

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