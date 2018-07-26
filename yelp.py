from botocore.vendored import requests
import json
try:
    #python2
    from urllib import urlencode
except ImportError:
    #python3
    from urllib.parse import urlencode

AUTH_TOKEN = 'isB958Rd1cSOaUSREJBtaJEKzsYvwUkpx0wxf56323V2udIzJoG1TNuB-oLMENDWX5Ve3qOL2iN82p3Qsoa9rgejPI2ypr5jOEu-wRX-fSrjTf2mK3TRiYCJrSJaW3Yx'

def getYelp(location):
    url = 'https://api.yelp.com/v3/businesses/search'
    query = {
        'radius': 1600,
        'location': location,
        'categories': 'restaurants',
        'limit': 50
    }

    url = url + '?' + urlencode(query)
    response = requests.get(url, headers={'Authorization': 'Bearer ' + AUTH_TOKEN})
    businesses = json.loads(response.text)['businesses']

    return businesses