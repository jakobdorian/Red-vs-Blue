import pandas as pd
import matplotlib.pyplot as plt
def create_agents(nx):
    print("creating agents...")

    # df = pd.read_csv('network-2.csv')
    Graphtype = nx.Graph()
    # g = nx.from_pandas_edgelist(df, edge_attr='weight', create_using=Graphtype)

    data = open('network-2.csv', "r")
    next(data, None)
    data2 = open('node-attributes', "r")
    next(data2, None)
    # print(data2)
    # skip first line

    # CREATE GRAPHS FOR EACH TEAM
    greenTeam_graph = nx.parse_edgelist(data, delimiter=',', create_using=Graphtype, nodetype=int, data=(('weight', float),))
    redTeam_graph = nx.Graph()
    redTeam_graph.add_node(26)
    blueTeam_graph = nx.Graph()
    blueTeam_graph.add_node(27)




    attrs_green = {'team': 'green'}
    attrs_blue = {'team': 'blue'}
    attrs_red = {'team': 'red'}
    attrs_grey_good = {'team': 'grey-good'}
    attrs_grey_bad = {'team': 'grey-bad'}

    greenTeam_graph.graph.update(attrs_green)
    blueTeam_graph.graph.update(attrs_blue)
    redTeam_graph.graph.update(attrs_blue)


    # nx.set_node_attributes(greenTeam_graph, attrs_green)

    # print(nx.info(greenTeam_graph))
    nx.draw(greenTeam_graph)
    nx.draw(redTeam_graph)
    plt.show()
