from typing import Union

from fastapi import FastAPI
from fastapi import HTTPException
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes cambiar esto a la lista de tus dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def read_root():
    return {"Hello": "World"}

async def scrape_website():
    url = "https://www.bcv.org.ve"  # URL específica que deseas scrape
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(url)
            response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        
        
        
        div_euro = soup.find('div', id='euro')
        euro = div_euro.find('strong').text
        euro_limpio = euro.replace(' ', '').replace(',', '.')
        valorEuro = float(euro_limpio)
        valorEuro_redondeado = round(valorEuro, 2)
        
        
        div_dolar = soup.find('div', id='dolar')
        dolar = div_dolar.find('strong').text
        dolar_limpio = dolar.replace(' ', '').replace(',', '.')
        ValorDolar = float(dolar_limpio)    
        valorDolar_redondeado = round(valorEuro, 2)
        
        
        div_yuan = soup.find('div', id='yuan')
        yuan = div_yuan.find('strong').text
        yuan_limpio = yuan.replace(' ', '').replace(',', '.')
        ValorYuan = float(yuan_limpio)    
        valorYuan_redondeado = round(ValorYuan, 2)
        
        
        div_lira = soup.find('div', id='lira')
        lira = div_lira.find('strong').text
        lira_limpio = lira.replace(' ', '').replace(',', '.')
        ValorLira = float(lira_limpio)    
        valorLira_redondeado = round(ValorLira, 2)
        
        div_rublo = soup.find('div', id='rublo')
        rublo = div_rublo.find('strong').text
        rublo_limpio = rublo.replace(' ', '').replace(',', '.')
        valorRublo = float(rublo_limpio)    
        valorRublo_redondeado = round(valorRublo, 2)
        
        
        
        
        
        # Aquí puedes personalizar la lógica para extraer la información que necesitas
        # en este ejemplo, simplemente obtenemos el título de la página
        title = soup.title.string.strip()

        return {"url": url, "title": title,"dolar":valorDolar_redondeado,"euro":valorEuro_redondeado,"yuan":valorYuan_redondeado,"Lira":valorLira_redondeado,"Rublo":valorRublo_redondeado}

    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Error al acceder a la URL: {str(e)}")
@app.get("/scrape")
async def scrape():
    result = await scrape_website()
    return result