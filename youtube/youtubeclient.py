import urllib.request
import urllib.parse
import json

API_KEY = 'AIzaSyBgz5Z_v3cc1iLE83SPttoPWcPmymWuktc'


def web_request(url, **params):
    headers = dict()
    headers['User-Agent'] = 'Music Recommendations'
    url_parsed = urllib.parse.urlparse(url)
    parameters = urllib.parse.parse_qs(url_parsed.query)
    for param in params:
        parameters[param] = params[param]
    parameters['key'] = API_KEY
    new_url = urllib.parse.urlunparse((url_parsed.scheme, url_parsed.netloc, url_parsed.path, url_parsed.params, urllib.parse.urlencode(parameters), ''))
    request = urllib.request.Request(new_url, headers=headers)
    response = urllib.request.urlopen(request)
    response_body = response.read().decode('utf-8')
    response.close()
    return json.loads(response_body)


def search_youtube(q):
    url = 'https://www.googleapis.com/youtube/v3/search?'
    response = web_request(url, part='snippet', q=q)
    return response['items']


def main():
    print(search_youtube('black hozzzle sun'))


if __name__ == "__main__":
    main()
