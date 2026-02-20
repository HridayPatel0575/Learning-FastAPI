from fastapi import FastAPI,Path,HTTPException,Query
import json

app = FastAPI()

def loader():
    with open('patient.json','r') as f:
        data=json.load(f)
    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id:str=Path(...,description='Id of the patient ex.P001')):
    data = loader()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail='Patient not found')

@app.get('/sort')
def sort_patient(sort_by:str=Query(...,description='sort on the basis of height,weight'),
                 order:str=Query('asc',description='sort in asc or desc order')):
    valid_field=['height','weight','bmi']

    if sort_by not in valid_field:
        raise HTTPException(status_code=400,detail='invalid field,select from {valid_field}')
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail='invalid field,select from ["asc","desc"]')
    
    data = loader()
    sorted_order =True if order=='desc'else False

    sorted_data = sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=sorted_order)

    return sorted_data