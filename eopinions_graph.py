import pandas as pd
import networkx as nx

wsv = pd.read_csv("soc-Epinions1.txt", delimiter="\t", header=0)
#  print(wsv)

G = nx.nx.from_pandas_edgelist(wsv, 'FromNodeId', 'ToNodeId')
#  print(G)

#  cl = list(nx.find_cliques(G))
#  st = sorted(cl, key=lambda cc: len(cc), reverse=True)

#   print(str(len(st[9])) + " -> " + str(st[9]))

#  print("degree_centrality--------------------------")
dc = nx.degree_centrality(G)
df2 = pd.DataFrame(dc.values(), columns=['DEGFEE_CENTRALITY'])
print(df2)
#  print(dc)

# too slow to run
#  print("closeness_centrality---------------------")
#  cs = nx.closeness_centrality(G)
#  print(cs)

# too slow
#  print("betweenness centrality------------------")
#  bc = nx.betweenness_centrality(G)
#  print(bc)

#  print("eigenvector centrality------------------")
ec = nx.eigenvector_centrality(G)
#  print(ec)
df = pd.DataFrame(ec.values(), columns=['EIGENVECTOR_CENTRALITY'])
print(df)

merged_df = df.merge(df2, left_index=True, right_index=True)
print(merged_df)

print(merged_df.corr())
