import urllib2
import urllib
import logging
log = logging.getLogger(__name__)

def post2FeUpdateEventCase(url, data):
    try:
        url_values = urllib.urlencode(data)
        full_url = url + '?' + url_values
        response = urllib2.urlopen(full_url)
        return  response.getcode()
    except urllib2.HTTPError, e:
        log.error(e)
        return e.code
