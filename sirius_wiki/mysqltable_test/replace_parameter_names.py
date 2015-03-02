#!/usr/bin/env python

"""
Replace parameter names from pages, according to correspondence in dictionary.
"""

import re
import pywikibot
import pywikibot.pagegenerators


PARAMETER_NS = 104
TABLE_NS = 118

PARAMETER_NS_STR = 'Parameter:'

RE_LINK_WITH_TEMPLATE = '\[\[[^\]]*\{[^\[]*\]\]'
RE_LINK_WITHOUT_TEMPLATE = '\[\[[^\]\{]*\]\]'
RE_TEMPLATE = '\{\{[^\{]*\}\}'

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
    'Storage ring beam gamma factor': 'SI beam gamma factor',
    'Storage ring horizontal tune': 'SI optics tune horizontal',
    'Storage ring vertical tune': 'SI optics tune vertical',
    'Storage ring number of long straight sections': 'SI lattice long straight section number',
}


def replace_parameters(text):
    text = replace_links_with_templates(text)
    text = replace_links(text)
    text = replace_templates(text)

    return text


def replace_links_with_templates(text):
    links = re.findall(RE_LINK_WITH_TEMPLATE, text)
    for link in links:
        templates = re.findall(RE_TEMPLATE, link)
        if not len(templates) == 1:
            continue

        repl = get_template_replacement(templates[0])
        if repl is not None:
            text = text.replace(link, repl)

    return text


def replace_links(text):
    links = re.findall(RE_LINK_WITHOUT_TEMPLATE, text)
    for link in links:
        repl = get_link_replacement(link)
        if repl is not None:
            text = text.replace(link, repl)

    return text


def replace_templates(text):
    templates = re.findall(RE_TEMPLATE, text)
    for t in templates:
        repl = get_template_replacement(t)
        if repl is not None:
            text = text.replace(t, repl)

    return text


def get_link_replacement(link):
    link = strip_link_braces(link)
    if not link.startswith(PARAMETER_NS_STR):
        return None

    parts = link.split('|')
    name = parts[0].lstrip(PARAMETER_NS_STR)
    if name not in TABLE:
        return None

    new_name = TABLE[name]
    if len(parts) == 1:
        return '[[' + PARAMETER_NS_STR + new_name + ']]'
    elif len(parts) == 2:
        return '[[' + PARAMETER_NS_STR + new_name + '|' + parts[1] + ']]'
    else:
        return None


def get_template_replacement(template):
    for T in TEMPLATES:
        if template.find(T) > 0:
            break
    else:
        return None

    for s in SPECIALISATIONS:
        if template.find(s) > 0:
            repl = get_specialised_template_replacement(template, s)
            break
    else:
        repl = get_specialised_template_replacement(template)

    return repl


def get_specialised_template_replacement(template, specialisation=None):
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


def strip_link_braces(link):
    return link.lstrip('[').rstrip(']')


if __name__ == '__main__':
    site = pywikibot.Site('en', 'siriuswiki')
    g = pywikibot.pagegenerators.AllpagesPageGenerator(
        site=site,
        namespace=TABLE_NS
    )

    i = 0
    pages = []
    for page in g:
        pages.append(page)
        i += 1

    page = pages[45]
    text = replace_parameters(page.text)

    print(text)
