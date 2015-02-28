#!/usr/bin/env python

"""Delete all pages from Parameter namespace."""

import time
import requests
import pywikibot
import pywikibot.pagegenerators
import password


PARAMETER_NS = 104

site = pywikibot.Site('en', 'siriuswiki')

g = pywikibot.pagegenerators.AllpagesPageGenerator(
    site=site,
    namespace=PARAMETER_NS
)

titles = []
for page in g:
    titles.append(page.title())

USER = 'afonso'
PASSWORD = password.password
BASEURL = 'http://10.0.21.163/mediawiki-1.23.1/api.php'
REASON = 'Change parameter naming scheme'

prms = '?action=login&lgname=%s&lgpassword=%s&format=json' % (USER, PASSWORD)

r1 = requests.post(BASEURL + prms)

token = r1.json()['login']['token']
prms += '&lgtoken=%s' % token

r2 = requests.post(BASEURL + prms, cookies=r1.cookies)

delete_token_prms = '?action=tokens&type=delete&format=json'
r3 = requests.post(BASEURL + delete_token_prms, cookies=r1.cookies)
delete_token = r3.json()['tokens']['deletetoken'].replace('+\\', '%2B%5C')

for title in titles:
    delete_prms = '?action=delete&title=%s&reason=%s&token=%s&format=json' % (title, REASON, delete_token)
    r4 = requests.post(BASEURL + delete_prms, cookies=r1.cookies)
    time.sleep(1)
    print(r4.json())
