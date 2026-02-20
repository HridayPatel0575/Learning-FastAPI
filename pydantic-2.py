from pydantic import BaseModel,Field,field_validator,EmailStr,model_validator
from typing import List,Dict

class Patient(BaseModel):
    name:str
    age:int
    email:EmailStr
    contact_details: Dict[str, str] = None

    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError('Patients older than 60 must have an emergency contact')
        return model    


def insert_patient_data(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.email)
    print(patient.contact_details)

Patient_info={'name':'Hriday','age':'90','email':'23aiml052@charusat.edu.in','contact_details':{'phone':'79','emergency':'81'}}

# Patient_info={'name':'Hriday','age':'66','email':'23aiml052@charusat.edu.in'}


patient1 = Patient(**Patient_info)
