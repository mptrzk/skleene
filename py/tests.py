from prev import re_dbg, re, lex

assert(re(['end'], '') == ('', None))
assert(re(['end'], 'a') == (None, None))

assert(re(['str', 'a'], 'a') == ('a', ''))
assert(re(['str', 'n'], 'a') == (None, None))
assert(re(['str', ''], 'a') == ('', 'a'))
assert(re(['str', 'aaaa'], '') == (None, None))
assert(re(['str', 'ab'], 'abcd') == ('ab', 'cd'))
assert(re(['str', 'abcd'], 'ab') == (None, None))

assert(re(['ran', 'a', 'c'], '') == (None, None))
assert(re(['ran', 'a', 'c'], 'a') == ('a', ''))
assert(re(['ran', 'a', 'c'], 'abc') == ('a', 'bc'))
assert(re(['ran', 'a', 'c'], 'bbc') == ('b', 'bc'))
assert(re(['ran', 'a', 'c'], 'cbc') == ('c', 'bc'))
assert(re(['ran', 'a', 'c'], 'dbc') == (None, None))

assert(re(['alt', ['str', 'a'], ['str', 'c']], '') == (None, None))
assert(re(['alt', ['str', 'a'], ['str', 'c']], 'a') == ('a', ''))
assert(re(['alt', ['str', 'a'], ['str', 'c']], 'abc') == ('a', 'bc'))
assert(re(['alt', ['str', 'a'], ['str', 'c']], 'bbc') == (None, None))
assert(re(['alt', ['str', 'a'], ['str', 'c']], 'cbc') == ('c', 'bc'))
assert(re(['alt', ['str', 'a'], ['str', 'c']], 'dbc') == (None, None))

#TODO and tests
assert(re(['and', ['str', 'abc'], ['str', 'ab']], 'abcd') == ('ab', 'cd'))
assert(re(['and', ['str', 'abc'], ['str', 'ab']], 'abdd') == (None, None))

assert(re(['seq', ['str', 'ab'], ['ran', 'a', 'c']], '') == (None, None))
assert(re(['seq', ['str', 'ab'], ['ran', 'a', 'c']], 'ab') == (None, None))
assert(re(['seq', ['str', 'ab'], ['ran', 'a', 'c']], 'abcd') == ('abc', 'd'))
assert(re(['seq', ['str', 'ab'], ['ran', 'a', 'c']], 'abdd') == (None, None))

assert(re(['rep', ['str', 'ab']], '') == ('', ''))
assert(re(['rep', ['str', 'ab'], 1], '') == (None, None))
assert(re(['rep', ['str', 'ab'], 1], 'ab') == ('ab', ''))
assert(re(['rep', ['str', 'ab'], 1], 'ababcd') == ('abab', 'cd'))
assert(re(['rep', ['str', 'ab'], 1, 1], 'ababcd') == (None, None))
assert(re(['rep', ['str', 'ab'], 1, 1], 'abcd') == ('ab', 'cd'))

assert(re(['not', ['str', 'ab']], '') == (None, None))
assert(re(['not', ['str', 'ab']], 'a') == ('a', ''))
assert(re(['not', ['str', 'ab']], 'aab') == ('a', 'ab'))
assert(re(['not', ['str', 'ab']], 'abb') == (None, None))

assert(re('wsc', '') == (None, None))
assert(re('wsc', 'Kk') == (None, None))
assert(re('wsc', ' Kk') == (' ', 'Kk'))
assert(re('wsc', '\tKk') == ('\t', 'Kk'))
assert(re('wsc', '\nKk') == ('\n', 'Kk'))
assert(re('wsc', '\rKk') == ('\r', 'Kk'))

assert(re('nl', '\r\nl') == ('\r\n', 'l'))
assert(re('nl', '\r\n\nl') == ('\r\n', '\nl'))

assert(re('numc', '') == (None, None))
assert(re('numc', '1') == ('1', ''))
assert(re('numc', '11') == ('1', '1'))
assert(re('numc', 'a1') == (None, None))

assert(re('alphac', '') == (None, None))
assert(re('alphac', '1') == (None, None))
assert(re('alphac', 'jk') == ('j', 'k'))
assert(re('alphac', 'Kk') == ('K', 'k'))

#TODO alphanumc, uint, int, float

#re_dbg(True)
assert(re('gap', '') == (None, None))
assert(re('gap', ' \t\n  \nfoo') == (' \t\n  \n', 'foo'))
assert(re('paragraph', 'f') == ('f', ''))
assert(re('paragraph', 'f   \n\ng') == ('f', '   \n\ng'))

with open('in') as f:
  tokens = lex(['gap', 'paragraph'], f.read())
  with open('out', 'w') as g:
    g.write(''.join(map(lambda x: x[1], tokens[::-1])))




print("all tests passed")

