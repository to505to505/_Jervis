from fastapi import FastAPI, Request
import requests
app = FastAPI()

@app.get('/', tags = ['ROOT'])
async def root() -> dict:
    return{'Ping': 'Pong'}  



@app.post('/return_image/', tags = ['POST'])
async def handle_post(request: Request):
    data = await request.json()
    # ...
    return {"message": "Data received and processed successfully"}



