def p(g):
 for i in range(1,len(g)):
  for j in range(len(g[0])):g[i][j]=g[i][j]or g[i-1][j]
 return g