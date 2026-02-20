from fastapi import FastAPI
import json

app = FastAPI()

def loader():
    with open('patient.json','r') as f:
        data=json.load(f)
    return data

@app.get('/')
def hello():
    return {'message':'patient api'}

@app.get('/home')
def home():
    return {'message':'home'}

@app.get('/view')
def view():
    data = loader()

    return data