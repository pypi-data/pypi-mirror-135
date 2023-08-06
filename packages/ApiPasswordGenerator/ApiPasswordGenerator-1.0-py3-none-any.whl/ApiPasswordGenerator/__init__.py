import requests



def get(number):
    r=requests.get(url='https://api.password-gen.ml/request?number='+str(number))
    print(r.text)

