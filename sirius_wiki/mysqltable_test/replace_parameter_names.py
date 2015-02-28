#!/usr/bin/env python

"""
Replace parameter names from pages, according to correspondence in dictionary.
"""

import re
import pywikibot
import pywikibot.pagegenerators


NS_PARAMETER = 104
NS_TABLE = 118

RE_PURE_LINK = '\[\[[^\]\{]*\]\]'
RE_LINK_WITH_TEMPLATE = '\[\[[^\]]*\{.*\]\]'
RE_TEMPLATE_VALUE = '\{\{Storage ring value[^\{]*\}\}'
RE_TEMPLATE_UNITS = '\{\{Storage ring units[^\{]*\}\}'
RE_TEMPLATE = '\{\{Storage ring[^\{]*\}\}'

MACHINES = {
    'Linac': 'LI',
    'Linac to booster transport line': 'TB',
    'Booster': 'BO',
    'Booster to storage ring transport line': 'TB',
    'Storage ring': 'SI'
}

SPECIALISATIONS = ['value', 'units']

TEMPLATES = []
for m in MACHINES.keys() + MACHINES.values():
    TEMPLATES.append(m)
    for s in SPECIALISATIONS:
        TEMPLATES.append(m + ' ' + s)

TABLE = {
    'Storage ring horizontal tune': 'SI optics tune horizontal',
    'Storage ring vertical tune': 'SI optics tune vertical'
}


def replace_parameters(text):
    # Find all templates
    templates = re.findall('\{\{[^\{]*\}\}', text)

    for t in templates:
        for T in TEMPLATES:
            if t.find(T) > 0:
                break
        else:
            continue

        for s in SPECIALISATIONS:
            if t.find(s) > 0:
                repl = get_template_replacement(t, s)
                break
        else:
            repl = get_template_replacement(t)

        if repl is not None:
            text = text.replace(t, repl)

    return text


def get_template_replacement(template, specialisation=None):
    t = strip_template_braces(template)
    s = t.split('|')

    tag = 'sirius'
    if specialisation is not None:
        tag += '_' + specialisation
        s[0] = s[0].rstrip(' ' + specialisation)

    # Replace short machine name by long name
    for item in MACHINES.items():
        if s[0] == item[1]:
            s[0] = item[0]
            break

    repl = '<' + tag

    if len(s) == 3:
        repl += ' format=' + s[2]
    repl += '>'

    name = s[0] + ' ' + s[1]
    if name in TABLE:
        name = TABLE[name]
    else:
        return None
    repl += name + '</' + tag + '>'

    return repl


def strip_template_braces(template):
    return template.lstrip('{').rstrip('}')


if __name__ == '__main__':
    site = pywikibot.Site('en', 'siriuswiki')
    g = pywikibot.pagegenerators.AllpagesPageGenerator(
        site=site,
        namespace=NS_TABLE
    )

    i = 0
    pages = []
    for page in g:
        pages.append(page)
        # print(str(i) + ': ' + page.title())
        i += 1

    page = pages[45]
    text = replace_parameters(page.text)

    print(text)
