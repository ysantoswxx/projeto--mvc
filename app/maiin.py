# Ponto de entrada do meu sistema
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from app.controllers import auth_controller

app = FastAPI(title="Sistema de ponto de vendas")

#Configurar a pasta para servir os arquivos estáticos (CSS, JS e IMG)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

#configurar o jinja2 para renderizar os Html
templates = Jinja2Templates(directory="app/templates")

#Incluir o routes dos controladores
app.include_router(auth_controller.router)



