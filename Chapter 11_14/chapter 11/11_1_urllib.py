from urllib import request
from urllib.parse import quote_plus

google = request.urlopen('https://google.com')
google = google.read()
print(google[:200])
url = 'http://google.com?q='
url_with_query = url + quote_plus('python web scraping')

web_search = request.urlopen(url_with_query)
web_search = web_search.read()

print(web_search[:200])
