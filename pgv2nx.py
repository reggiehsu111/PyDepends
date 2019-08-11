import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph(nx.read_dot('file_structure.dot'))
nx.draw(G,pos,with_labels=True)
plt.show()