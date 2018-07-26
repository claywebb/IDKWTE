import requests
import json
try:
    #python2
    from urllib import urlencode
except ImportError:
    #python3
    from urllib.parse import urlencode

AUTH_TOKEN = ''

def getYelp(location):
    url = 'https://api.yelp.com/v3/businesses/search'
    query = {
        'radius': 1600,
        'location': location,
        'categories': 'restaurants'
    }

    url = url + '?' + urlencode(query)
    response = requests.get(url, headers={'Authorization': 'Bearer ' + AUTH_TOKEN})
    businesses = json.loads(response.text)

    return businesses

print json.dumps(getYelp('Amazon Spheres'))