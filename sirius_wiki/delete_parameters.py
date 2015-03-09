#!/usr/bin/env python

"""Delete all pages from Parameter namespace."""

import time
import requests
import pywikibot
import pywikibot.pagegenerators
import config


PARAMETER_NS = 104

site = pywikibot.Site('en', 'siriuswiki')

g = pywikibot.pagegenerators.AllpagesPageGenerator(
    site=site,
    namespace=PARAMETER_NS
)

titles = []
for page in g:
    titles.append(page.title())

USER = config.user
PASSWORD = config.password
BASEURL = config.baseurl + 'api.php'
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
