from prev import re

assert(re(['str', 'a'], 'a') == ('a', ''))
assert(re(['str', 'n'], 'a') == (None, 'a'))
assert(re(['str', ''], 'a') == ('', 'a'))
assert(re(['str', 'aaaa'], '') == (None, ''))
assert(re(['str', 'ab'], 'abcd') == ('ab', 'cd'))
assert(re(['str', 'abcd'], 'ab') == (None, 'ab'))

assert(re(['ran', 'a', 'c'], '') == (None, ''))
assert(re(['ran', 'a', 'c'], 'a') == ('a', ''))
assert(re(['ran', 'a', 'c'], 'abc') == ('a', 'bc'))
assert(re(['ran', 'a', 'c'], 'bbc') == ('b', 'bc'))
assert(re(['ran', 'a', 'c'], 'cbc') == ('c', 'bc'))
assert(re(['ran', 'a', 'c'], 'dbc') == (None, 'dbc'))

assert(re(['alt', ['str', 'a'], ['str', 'c']], '') == (None, ''))
assert(re(['alt', ['str', 'a'], ['str', 'c']], 'a') == ('a', ''))
assert(re(['alt', ['str', 'a'], ['str', 'c']], 'abc') == ('a', 'bc'))
assert(re(['alt', ['str', 'a'], ['str', 'c']], 'bbc') == (None, 'bbc'))
assert(re(['alt', ['str', 'a'], ['str', 'c']], 'cbc') == ('c', 'bc'))
assert(re(['alt', ['str', 'a'], ['str', 'c']], 'dbc') == (None, 'dbc'))

assert(re(['seq', ['str', 'ab'], ['ran', 'a', 'c']], '') == (None, ''))
assert(re(['seq', ['str', 'ab'], ['ran', 'a', 'c']], 'ab') == (None, 'ab'))
assert(re(['seq', ['str', 'ab'], ['ran', 'a', 'c']], 'abcd') == ('abc', 'd'))
assert(re(['seq', ['str', 'ab'], ['ran', 'a', 'c']], 'abdd') == (None, 'abdd'))

assert(re(['rep', ['str', 'ab']], '') == ('', ''))
assert(re(['rep', ['str', 'ab'], 1], '') == (None, ''))
assert(re(['rep', ['str', 'ab'], 1], 'ab') == ('ab', ''))
assert(re(['rep', ['str', 'ab'], 1], 'ababcd') == ('abab', 'cd'))
assert(re(['rep', ['str', 'ab'], 1, 1], 'ababcd') == (None, 'ababcd'))
assert(re(['rep', ['str', 'ab'], 1, 1], 'abcd') == ('ab', 'cd'))

assert(re(['not', ['str', 'ab']], '') == ('', ''))
assert(re(['not', ['str', 'ab']], 'a') == ('a', ''))
assert(re(['not', ['str', 'ab']], 'aab') == ('a', 'ab'))
assert(re(['not', ['str', 'ab']], 'abb') == (None, 'abb'))

assert(re('numc', '') == (None, ''))
assert(re('numc', '1') == ('1', ''))
assert(re('numc', '11') == ('1', '1'))
assert(re('numc', 'a1') == (None, 'a1'))

print("all tests passed")



