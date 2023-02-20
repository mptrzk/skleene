
def re_end(s):
  if s == '':
    return '', ''
  return None, s

def re_str(expr, s):
  ss = s[:len(expr)]
  if ss == expr:
    return ss, s[len(expr):] 
    #It doesn't throw "out of range", because if end in a slice is greater then the length,
    #it just returns the whole string. 
    #TODO describe why the condition makes it impossible for the 2nd slice to be invalid 
  else:
    return None, s

def re_ran(lo, hi, s):
  if s == '':
    return None, s
  c = s[0]
  rst = s[1:]
  if (ord(c) >= ord(lo) and ord(c) <= ord(hi)):
    return c, rst
  return None, s

def re_alt(exprs, s):
  for expr in exprs:
    val, rst = re(expr, s)
    if val != None:
      return val, rst
  return None, s

def re_and(exprs, s):
  for expr in exprs:
    val, rst = re(expr, s)
    if val == None:
      return None, s
  else:
    return val, rst

def re_seq(exprs, s):
  val_acc = ''
  rst = s
  for expr in exprs:
    val, rst = re(expr, rst)
    if val == None:
      return None, s
    val_acc += val
  return val_acc, rst

def re_rep(expr, lo, hi, s):
  val_acc = ''
  rst = s
  i = 0
  while hi == None or i <= hi:
    val, rst = re(expr, rst)
    if val == None:
      if lo == None or i >= lo:
        return val_acc, rst #rst should be OK, because misses should always return the input string
      return None, s
    val_acc += val
    i += 1
  return None, s

def re_not(expr, s):
  val, rst = re(expr, s) #returning tuple shenanigans
  if val == None:
    return (s[0], s[1:]) if s else ('', '')
  return None, s


re_defs = {
  'wsc' : ['ran', chr(0), ' '],
  'nl' : ['alt', ['str', '\r\n'], ['str', '\n']],
  'numc': ['ran', '0', '9'],
  'alphac': ['alt', ['ran', 'a', 'z'], ['ran', 'A', 'Z']],
  'alphanumc': ['alt', 'numc', 'alphac'],
  'gap' : ['rep', ['seq', ['rep', 'iwsc'], ['alt', 'nl', ['end']]], 1],
}

def re(expr, s):
  if type(expr) == str:
    #TODO "expression not expanded, use an expanded expression or re-ex function"
    return re(re_defs[expr], s)
  if type(expr) == list:
    op, *args = expr
    if op == 'end':
      return re_end(s)
    if op == 'str':
      return re_str(args[0], s)
    if op == 'ran':
      return re_ran(*args, s)
    if op == 'alt':
      return re_alt(args, s)
    if op == 'and':
      return re_and(args, s)
    if op == 'seq':
      return re_seq(args, s)
    if op == 'rep':
      lo = args[1] if len(args) >= 2 else None
      hi = args[2] if len(args) >= 3 else None
      return re_rep(args[0], lo, hi, s)
    if op == 'not':
      return re_not(args[0], s)

def lex(rules, text):
  res = []
  while text:
    for r in rules:
      val, text = re(r, text)
      if val != None:
        res.append([r, val])
        break
    else:
      raise Exception("no rules match the following text:")
      #TODO sane way to display
  return res

