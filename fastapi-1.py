from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def hello():
    return {'message':'hello'}

@app.get('/home')
def home():
    return {'message':'home'}