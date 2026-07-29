from fastapi import FastAPI
app = FastAPI()
@app.get("/clientes")
def ola_mundo():
    return {'mensagem': 'minha primeira api em fastapi'}

@app.get("/sobre")
def get_sobre():
    return {'mensagem': 'sobre a api'}