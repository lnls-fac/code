# -*- coding: utf-8 -*-

class Parameter:

    def __init__(self, name, group='FAC', symbol='', is_derived=False, value=None, units='', deps='', obs=''):
        self.name        = name
        self.group       = group
        self.symbol      = symbol
        self.is_derived  = is_derived
        self.value       = value
        self.units       = units
        self.deps        = deps
        self.obs         = obs
        #self.DEFAULT_OBS = 'Automatically generated, manual changes may be overwritten. Comments may be added in the [[Parameter_Talk:' + self.name + '|Discussion]] section of this page.'

    def __str__(self):
        r = (self.name + ': ' + str(self.value) + ' ' + self.units)
        return r

    def __lt__(self, other):
        if self.name.lower() < other.name.lower():
            return True
        else:
            return False

    def create_wiki_deps(self):
        deps = ''
        for dep in self.deps:
            if deps is not '':
                deps = deps + ', '
            deps = deps + '[[Parameter:' + str(dep) + '|' + str(dep) + ']]'
        return deps

    def create_wiki_page(self):
        wiki = []
        wiki.append('==Data==')
        wiki.append('<section begin=data/>')
        wiki.append('* Group: <section begin=group/>' + self.group + '<section end=group/>')
        wiki.append('* Symbol: <section begin=symbol/>' + self.symbol + '<section end=symbol/>')
        wiki.append('* Derived: <section begin=is_derived/>' + str(self.is_derived) + '<section end=is_derived/>')
        wiki.append('* Value: <section begin=value/>' + str(self.value) + '<section end=value/>')
        wiki.append('* Units: <section begin=units/>' + self.units + '<section end=units/>')
        wiki.append('* Dependencies: <section begin=deps/>' + self.create_wiki_deps() + '<section end=deps/>')
        wiki.append('<section end=data/>')
        wiki.append('==Observations==')
        wiki.append('<section begin=obs/>' + self.create_obs() + '<section end=obs/>')
        text = '\n'.join(wiki)
        #print(text)
        return text

    def create_obs(self):
        obs = ''
        for s in self.obs:
            obs += '* ' + s + '\n'
        #obs += '* ' + self.DEFAULT_OBS + '\n'
        return obs
