import urllib.request
import urllib.parse
import json


def web_request(url, **params):
    headers = dict()
    headers['User-Agent'] = 'Music Recommendations'

    url_parsed = urllib.parse.urlparse(url)
    parameters = urllib.parse.parse_qs(url_parsed.query)
    for param in params:
        parameters[param] = params[param]
    parameters['format'] = 'json'
    new_url = urllib.parse.urlunparse((url_parsed.scheme, url_parsed.netloc, url_parsed.path, url_parsed.params, urllib.parse.urlencode(parameters), ''))
    request = urllib.request.Request(new_url, headers=headers)
    response = urllib.request.urlopen(request)
    response_body = response.read().decode('utf-8')
    response.close()
    return json.loads(response_body)


def search_tags(type):
    url = 'http://musicovery.com/api/V6/tag.php'
    response = web_request(url, fct='search', type='mood')
    tags = list()
    for i in response['tags']['tag']:
        if i.isdigit():
            if response['tags']['tag'][i]['language'] == "en":
                tags.append(response['tags']['tag'][i]['name'])
    return tags


def get_moods():
    return search_tags('mood')


def playlist(**params):
    url = 'http://musicovery.com/api/V6/playlist.php'
    return web_request(url, **params)['tracks']['track']


def playlist_from_tag(tag):
    return playlist(fct='getfromtag', tag=tag, listenercountry='us')


def playlist_from_tag(tag, popularity_min, popularity_max):
    return playlist(fct='getfromtag', tag=tag, popularitymin=popularity_min,
                    popularitymax=popularity_max, listenercountry='us')


def playlist_from_tag(tag, popularity_min, popularity_max, year_min, year_max):
    return playlist(fct='getfromtag', tag=tag, yearmin=year_min, yearmax=year_max,
                    popularitymin=popularity_min, popularitymax=popularity_max, listenercountry='us')


def main():
    print(playlist_from_tag('sad', 75, 100, 1990, 1998))


if __name__ == "__main__":
    main()
