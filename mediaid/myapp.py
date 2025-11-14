import requests
import json

URL = "http://127.0.0.1:8000/doctorapi/"

def get_data(id = None):
    data = {}
    if id is not None:
        data = {'id':id}
    json_data = json.dumps(data)
    r = requests.get(url = URL, data = json_data)
    data = r.json()
    print(data)

# get_data()

def post_data():
    data = {
    'users' : '13',
    'name' : 'smith',
    'gender' : 'Male',
    'number' : 'hjbdhjbjc',
    'licensenum' : 'hbchj',
    'hospital' : 'bdhjcbd',
    'speciality' : 'hvhjd',
    'qualification' : "vvhvd",
    'availability' : 'Friday-Monday',
    'start' : "6:00 PM",
    'end' : "12:00 PM",
    'fees': 1000
    }

    json_data = json.dumps(data)
    r = requests.post(url = URL, data = json_data)
    data = r.json()
    print(data)

post_data()