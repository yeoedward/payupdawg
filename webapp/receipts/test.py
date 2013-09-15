def insert((x,m),L):
  if L == []:
    return [x]
  (a,m2) = L.pop(0)
  if x <= a:
    return [(x,m),(a,m2)]+L
  return [(a,m2)] + insert((x,m),L)

def del_eql(L):
  trans = []
  to_del = set()
  S = {}
  for (i,(n,m)) in enumerate(L):
    if n == 0:
      to_del.add(i)
    if -n in S:
      to_del.add(S[-n][0])
      to_del.add(i)
      payer = m if i > S[-n][0] else S[-n][1]
      payee = S[-n][1] if i > S[-n][0] else m
      trans += [(m,S[-n][1],abs(n))]
      del S[-n]
    else:
      S[n] = (i,m)
  result = []
  for (i,p) in enumerate(L):
    if i in to_del:
      continue
    result += [p]
  return (result,trans)

def matchmake(L):
  (result,trans) = del_eql(L)
  if len(result) == 0: return result + trans
  assert(len(result) != 1)
  (n1,m1) = result.pop()
  (n2,m2) = result.pop(0)
  new_n = n1 + n2
  new_m = m1 if abs(n1) >= abs(n2) else m2
  changed_hands = min(abs(n1),abs(n2))
  payer = m1 if n1 > 0 else m2
  payee = m2 if n1 > 0 else m1
  return trans + [(payer,payee,changed_hands)] + matchmake(insert((new_n,new_m),result))

