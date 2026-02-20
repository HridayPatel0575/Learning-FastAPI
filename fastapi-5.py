from fastapi import FastAPI,HTTPException,Path,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional

import json

app = FastAPI()

def loader():
    with open('patient.json','r') as f:
        data=json.load(f)
    return data

def save_data(data):
    with open('patient.json','w') as f:
        json.dump(data,f)


class Patient(BaseModel):

    id: Annotated[str, Field(..., description='ID of the patient', examples=['P001'])]
    name: Annotated[str, Field(..., description='Name of the patient')]
    city: Annotated[str, Field(..., description='City where the patient is living')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the patient')]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='Height of the patient in mtrs')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the patient in kgs')]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:

        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Obese'
        
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]

@app.get('/view')
def view():
    data = loader()

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

@app.post('/create')
def create_patient(patient:Patient):
    data = loader()

    if patient.id in data:
        raise HTTPException(status_code=400,detail='Patient already exists')
    
    data[patient.id]=patient.model_dump(exclude=['id'])

    save_data(data)

    return JSONResponse(
    status_code=200,
    content={"message": "Patient created successfully"})

    
@app.put('/edit/{patient_id}')
def update_patient(patient_id:str,patient_update:PatientUpdate):
    data = loader()
    if patient_id not in data:
        raise HTTPException(status_code=404,details='patient not found')
    
    existing_patient_info =data[patient_id]

    update_patient_info=patient_update.model_dump(exclude_unset=True)

    for key,value in update_patient_info.items():
        existing_patient_info[key] =value
    
    existing_patient_info['id']=patient_id
    patient_pydantic_object=Patient(**existing_patient_info)
    existing_patient_info=patient_pydantic_object.model_dump(exclude='id')
    data[patient_id] =existing_patient_info

    save_data(data)

    return JSONResponse(status_code=200,content={'message':'Info updated'})


@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str):
    data=loader()

    if patient_id not in data:
        raise HTTPException(status_code=404,detail='patient not found')
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200,content={'message':'patient_deleted'})