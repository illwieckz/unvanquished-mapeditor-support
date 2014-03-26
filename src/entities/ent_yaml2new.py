#!/usr/bin/env python3

starting_text = \
'''// !!! THIS FILE IS AUTOGENERATED, DO NOT EDIT
// Unvanquished entity definitions file for GTKRadiant 1.5/NetRadiant
// Update 2012-08-22 by Ingar: created template entities.def for Unvanquished

// Based on Tremulous entity definition file for GTKRadiant
// by Tim Angus <tma@op.ath.cx> 2003-09-08
// Update 2007-01-24 by Warrior: removed some references to bots, added
// the team_alien_hive entity and fixed team_alien_acid_tube coordinates.
// Update 2009-02-14 by Ingar: merged gpp1 entities.def

// Based on entities.def from GTKRadiant 1.3.11 which in turn is based on...
// Based on draft by Suicide 20 1999-07-30 and inolen 1999-09-03
// Upgraded by Eutectic: eutectic@ritualistic.com
// (visible models added by raYGunn - paths provided by Suicide 20)
// (terrain information added to func_group entity by Paul Jaquays)
// Q3Map2 entitys/keys added by ydnar
'''

# https://github.com/TTimo/GtkRadiant/issues/262
dont_place_dummy_flag = True

import yaml
import re
import sys

bad_token_re = re.compile(r'[}{)(\':\s]', re.M)

def escape_token(t):
    if bad_token_re.search(t):
        if t.find('"') >= 0:
            raise Exception('Bad token: {}'.format(t))
        return '"{}"'.format(t)
    return t

def color_to_float_triple(h):
    hexes = [h[:2], h[2:4], h[4:]]
    return [round(int(x, 16) / 255.0, 3) for x in hexes]

float_fmt = '{:.3f}'
heading = '------ {} ------'

def list_of_dicts_to_list_of_tuples(dd):
    res = []
    for d in dd:
        for k, v in d.items():
            res.append((k, v))
            break
    return res

def print_entity(e):
    name = escape_token(e['name'])
    color = '(F F F)'.replace('F', float_fmt).format(*color_to_float_triple(e['color']))
    e['flags'] = list_of_dicts_to_list_of_tuples(e['flags'])
    flags = [escape_token(k) for k, _ in e['flags']]
    if 'size_min' in e and 'size_max' in e:
        sizes = ' (F F F) (F F F)'.replace('F', float_fmt).format(*(e['size_min'] + e['size_max']))
    else:
        sizes = ''
        if not dont_place_dummy_flag:
            flags.insert(0, escape_token('?'))
    flags = ' '.join(flags)
    if flags:
        flags = ' ' + flags
    print('/*QUAKED {} {}{}{}'.format(name, color, sizes, flags))

    flags = []
    for k, v in e['flags']:
        if k == '-' or not v:
            continue
        flags.append('{}: {}'.format(k, v))
    if flags:
        print(heading.format('FLAGS'))
        for v in flags:
            print(v)

    props = []
    for k, v in sorted(e['props'].items()):
        props.append('{}: {}'.format(k, v))
    if props:
        print(heading.format('PROPERTIES'))
        for v in props:
            print(v)

    if e['desc']:
        print(heading.format('DESCRIPTION'))
        print(e['desc'])

    if e['specials']:
        for k, v in e['specials'].items():
            print('{}="{}"'.format(k, v))

    print('*/')
    print()

filename = sys.argv[1]

with open(filename, 'r') as f:
    text = f.read()
    elist = yaml.load(text)
    print(starting_text)
    for e in elist:
        print_entity(e)

