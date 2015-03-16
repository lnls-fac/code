#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


DEF_FILENAME = 'definitions_default.py'
OLD_FILENAME = 'sirius_ts.py'
NEW_FILENAME = 'sirius_ts_new.py'

PRM_LINESTART = '# Parameter'


f = open(DEF_FILENAME, 'r')
defs = f.readlines()
f.close()

f = open(OLD_FILENAME, 'r')
text = f.readlines()
f.close()

f = open(NEW_FILENAME, 'w')
new_text = ''.join(text)

prm_lines = []
for line in text:
    if line.lstrip().startswith(PRM_LINESTART):
        prm_lines.append(line)

for line in prm_lines:
    fields = line.split(',')
    is_derived = fields[2].strip()
    value = fields[3].strip()
    if '"' in value:
        continue
    else:
        value = value.split('.')[1]

    for d in defs:
        if value == d.split('=')[0].strip():
            break

    d = d.strip()

    if '"' in d:
        new_is_derived = 'is_derived=True'
        eq = d.split('=')[1].split('#')[0].strip()
        new_value = 'value=\'' + eq + '\''
        new_deps = 'deps=[]'
    else:
        new_is_derived = 'is_derived=False'
        new_value = None
        new_deps = None

    new_line = line.replace(is_derived, new_is_derived)
    if new_value is not None:
        new_line = re.sub('value=.*, *symbol', new_value + ', symbol', new_line)
    if new_deps is not None:
        new_line = re.sub('deps=\[.*\]{1}', new_deps, new_line)

    new_text = new_text.replace(line, new_line)

f.write(new_text)
f.close()
