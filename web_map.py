import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl
import folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderTimedOut


def data(acct):
    """
    (str) -> list
    Return list of tuples with data from twitter account.
    Tuple consists of user's name and location
    """

    TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    if (len(acct) < 1):
        acct = input('Please enter Twitter Account:')

    url = twurl.augment(TWITTER_URL,
                        {'screen_name': acct, 'count': 200})

    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()

    js = json.loads(data)

    lst = []
    for u in js['users']:
        name = u["name"]
        location = u["location"]
        lst.append((name, location))

    return lst


def create_map(lst):
    """
    (lst) -> None
    This function creates map with markers
    as html-file using list of names and locations

    """
    geolocator = Nominatim(user_agent="specify_your_app_name_here")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    map = folium.Map()
    lay = folium.FeatureGroup(name="Friends_map")

    for el in lst:
        try:
            location = geolocator.geocode(el[1])
            if location != None:
                lat, long = location.latitude, location.longitude
                lay.add_child(folium.Marker(location=[lat, long], popup=el[0],
                                            icon=folium.Icon()))
        except GeocoderTimedOut:
            continue

    map.add_child(lay)

    map.save("templates/map.html")
