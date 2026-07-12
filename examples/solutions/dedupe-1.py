from itertools import groupby
def p(g):
 w=len(g[0]);o=[]
 for r in g:
  x=[k for k,_ in groupby(r)if k];o+=[x+[0]*(w-len(x))]
 return o