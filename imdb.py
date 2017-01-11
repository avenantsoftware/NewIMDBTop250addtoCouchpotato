#!/usr/bin/env python
import hashlib, requests, httplib, urllib, urllib2, re
from lxml.html import parse
from BeautifulSoup import BeautifulSoup
from datetime import datetime

url = parse('http://www.took.nl/250/').getroot()
html_page = urllib2.urlopen("http://250.took.nl")

# verstuur pushover bericht
def pushover(str,str2):
  conn = httplib.HTTPSConnection("api.pushover.net:443")
  conn.request("POST", "/1/messages.json",
  urllib.urlencode({
    "token": "yourapitokenhere",
    "user": "youruserkeyhere",
    "message": str,
    "title" : str2,
    }), { "Content-type": "application/x-www-form-urlencoded" })
  conn.getresponse()
  return;

# haal benodigte shit uit html
aantal = url.cssselect("strong")[3].text_content()
nummer = url.cssselect("b")[0].text_content()
nummer = nummer.replace('.','')
film = url.cssselect("a")[54].text_content()
jaar = url.cssselect("a")[55].text_content()
bericht1 = film + " (" + jaar + ")"
bericht2 = film + " (" + jaar + ") toegevoegt aan couchpotato"
titel = "Nieuw op nummer: " + nummer  
soup = BeautifulSoup(html_page)
link = soup.find('a', href=re.compile('^http://www.imdb.com/title/'))['href']
link = link.replace('http://www.imdb.com/title/','')

# check het jaartal
huidigjaar = datetime.now().year

# Genereer MD5 hash van de meest recente titel
lasthash = hashlib.md5(film).hexdigest()

#with open('/var/opt/ihash.txt', 'r') as r:
with open('/home/htpc/Scripts/imdb/ihash.txt', 'r') as r:
  regel = r.readline()

if regel != lasthash:
  # sla nieuwe hash op
  #with open('/var/opt/ihash.txt', 'w') as w:
  with open('/home/htpc/Scripts/imdb/ihash.txt', 'w') as w:
    w.write(lasthash)
    # stuur pushover bericht
    if aantal != "0":
      if huidigjaar == int(jaar):
        pushover(bericht2,titel);
        couchpotato = "http://couchpotatoip:port/api/yourcouchpotatoapikeyhere/movie.add/?identifier=" + link
        requests.get(couchpotato) # stuur imdb id van film naar couchpotato
        print "film: " + film +  " (" + jaar + ") met imdb code: " + link + " ,toegevoegt aan couchpotato"
      else:
        pushover(bericht1,titel);
