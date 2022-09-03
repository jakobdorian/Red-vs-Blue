import pandas as pd
import matplotlib.pyplot as plt
def create_agents(nx):
    print("creating agents...")

    # df = pd.read_csv('network-2.csv')
    Graphtype = nx.Graph()
    # g = nx.from_pandas_edgelist(df, edge_attr='weight', create_using=Graphtype)

    data = open('network-2.csv', "r")
    # skip first line
    next(data, None)
    g = nx.parse_edgelist(data, delimiter=',', create_using=Graphtype, nodetype=int, data=(('weight', float),))

    print(nx.info(g))
    nx.draw(g)
    plt.show()