from pydantic import BaseModel

class Address(BaseModel):
    city:str
    state:str
    pincode:str

class Patient(BaseModel):
    name:str
    age:int
    address:Address

address_dict={'city':'Ahm','state':'gujarat','pincode':'380001'}

Address1 = Address(**address_dict)

def insert_patient_data(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.address)

Patient_info={'name':'Hriday','age':'90','address':Address1}

# Patient_info={'name':'Hriday','age':'66','email':'23aiml052@charusat.edu.in'}


patient1 = Patient(**Patient_info)

insert_patient_data(patient1)