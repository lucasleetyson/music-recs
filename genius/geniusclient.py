import urllib.request
import urllib.parse
import json

API_TOKEN = 's6dofbetBGkrsJ0OQH5IPEEyLla4XJ9-iHVTyMy01h1Jvl_1b_spO4cTQ09Me2T1'


def web_request(url, **params):
    headers = dict()
    headers['User-Agent'] = 'Music Recommendations'
    headers['Authorization'] = 'Bearer ' + API_TOKEN
    url_parsed = urllib.parse.urlparse(url)
    parameters = urllib.parse.parse_qs(url_parsed.query)
    for param in params:
        parameters[param] = params[param]
    new_url = urllib.parse.urlunparse((url_parsed.scheme, url_parsed.netloc, url_parsed.path, url_parsed.params, urllib.parse.urlencode(parameters), ''))
    request = urllib.request.Request(new_url, headers=headers)
    response = urllib.request.urlopen(request)
    response_body = response.read().decode('utf-8')
    response.close()
    return json.loads(response_body)


def search(q):
    url = 'https://api.genius.com/search'
    response = web_request(url, q=q)
    return response


def main():
    response = search('black hole sun')



if __name__ == "__main__":
    main()
