import os
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response, JSONResponse , HTMLResponse
from fastapi.encoders import jsonable_encoder
from typing import  List
import motor.motor_asyncio
from routers import create, getAllDetails , getDetailsByZipcode ,getDetailsByDate ,getDetailsByLocation , getDetailsFromAtomosome
import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static/templates")

# @app.on_event("startup")
# async def start_db():
#     await init_db()

app.include_router(create.router)
app.include_router(getAllDetails.router)
app.include_router(getDetailsByZipcode.router)
app.include_router(getDetailsByDate.router)
app.include_router(getDetailsByLocation.router)
app.include_router(getDetailsFromAtomosome.router)



@app.get("/")
def homepage(request: Request):
    #return   {"home": "This is the Air Monitoring REST API site!!!"}
    home="This is the Air Monitoring REST API site!!!"
    return templates.TemplateResponse("index.html", {"request": request, "message": home})



 # at last, the bottom of the file/module
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5049)