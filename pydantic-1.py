from pydantic import BaseModel,Field,field_validator,EmailStr
from typing import List

class Patient(BaseModel):
    name:str
    age:int
    email:EmailStr
     
    @field_validator('email')
    @classmethod
    def email_validator(cls,value):
        valid_domains=['charusat.edu.in']
        domain_name= value.split('@')[-1]

        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')
        return value
    
    @field_validator('name')
    @classmethod
    def name_uppercase(cls,value):
        return value.upper()

def insert_patient_data(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.email)

Patient_info={'name':'Hriday','age':'30','email':'23aiml052@charusat.edu.in'}


patient1 = Patient(**Patient_info)

insert_patient_data(patient1)