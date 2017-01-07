import urllib2
import urllib
import logging
import time

log = logging.getLogger(__name__)
def post2FeUpdateEventCase(url, data):
    mtries, mdelay, backoff = 4, 3, 2
    resp_code = 200
    while mtries > 1:
        try:
            url_values = urllib.urlencode(data)
            full_url = url + '?' + url_values
            response = urllib2.urlopen(full_url)
            resp_code = response.getcode()
            mtries = 1
        except urllib2.HTTPError as e:
            msg = "%s, Retrying in %d seconds..." % (str(e),mdelay)
            print('msg="%s"' % msg)
            resp_code = e.code
            time.sleep(mdelay)
            mdelay *= backoff
            mtries -= 1 
        except Exception as e:
            msg = "%s, Retrying in %d seconds..." % (str(e),mdelay)
            print('msg="%s"' % msg)
            log.warning(msg)
            if mtries == 2:
                resp_code = 500
                log.error(str(e))
            time.sleep(mdelay)
            mdelay *= backoff
            mtries -= 1 
    return resp_code
