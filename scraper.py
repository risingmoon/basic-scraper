import requests
from bs4 import BeautifulSoup
import sys
import json
FILENAME = 'apartments.html'


def fetch_search_results(
    query=None, minAsk=None, maxAsk=None, bedrooms=None
):
    """Fetches a request on Craigslist based on search parameter,
    and write the response as a FILENAME (html). and returns content
    and encoding values"""
    search_params = {
        key: val for key, val in locals().items() if val is not None
    }
    if not search_params:
        raise ValueError("No valid keywords")

    base = 'http://seattle.craigslist.org/search/apa'
    resp = requests.get(base, params=search_params, timeout=3)
    resp.raise_for_status()  # <- no-op if status==200
    #write to folder
    with open(FILENAME, 'w') as outfile:
        outfile.write(resp.content)
    return resp.content, resp.encoding


def read_search_results(filename=FILENAME):
    """Reads written html html and returns html and encoding strings"""
    with open(filename, 'r') as outfile:
        html = outfile.read()
    return html, 'utf-8'


def parse_source(html, encoding='utf-8'):
    """Parses html file and returns as a BeautifulSoup object"""
    parsed = BeautifulSoup(html, from_encoding=encoding)
    return parsed


def extract_listings(parsed):
    """Extracts location, link, description, price, and size
    from BeautifulSoup object and returns as a dictionary."""
    location_attrs = {'data-latitude': True, 'data-longitude': True}
    listings = parsed.find_all('p', class_='row', attrs=location_attrs)
    extracted = []
    for listing in listings:
        location = {key: listing.attrs.get(key, '') for key in location_attrs}
        link = listing.find('span', class_='pl').find('a')
        price_span = listing.find('span', class_='price')
        this_listing = {
            'location': location,
            'link': link.attrs['href'],
            'description': link.string.strip(),
            'price': price_span.string.strip(),
            'size': price_span.next_sibling.strip(' \n-/')
        }
        yield this_listing


def add_address(listing):
    api_url = 'http://maps.googleapis.com/maps/api/geocode/json'
    loc = listing['location']
    latlng_tmpl = "{data-latitude},{data-longitude}"
    parameters = {
        'sensor': 'false',
        'latlng': latlng_tmpl.format(**loc),
    }
    resp = requests.get(api_url, params=parameters)
    resp.raise_for_status()
    data = json.loads(resp.text)
    if data['status'] == 'OK':
        best = data['results'][0]
        listing['address'] = best['formatted_address']
    else:
        listing['address'] = 'unavailable'
    return listing

if __name__ == '__main__':
    import pprint
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        html, encoding = read_search_results('apartments.html')
    else:
        html, encoding = fetch_search_results(
            minAsk=500, maxAsk=1000, bedrooms=2
        )
    doc = parse_source(html, encoding)
    print type(doc)
    for listing in extract_listings(doc):
        listing = add_address(listing)
        pprint.pprint(listing)
