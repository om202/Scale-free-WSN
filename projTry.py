#Imported Packages
#import numpy as np
import random as rnd
import matplotlib.pyplot as plt
import networkx as nx
import collections

###### GLOBAL VARIABLES ######
nodes = [] #nodes list 
D = 500 #Max size of WSN deployment area
N = 250#Number of Nodes
R = 60 #Radius of transmission 
##############################

####### FUNCTIONS ######## 

#function to sort values in the nodes
def sorti(n):
    return(sorted(nodes,key=lambda x:x[0])) #sorting via 'x'
    
def distance(i,j):
    x = abs(i[0]-j[0])
    y = abs(i[1]-j[1])
    d = (x**2 + y**2)**(1/2)
    return d    

def neighbour():
    nodes_nbr = {} #dict of nbrs
    temp_nodes = nodes.copy()
    for i in nodes:
        temp_nbr = []
        for j in temp_nodes:
            if distance(i,j) < R and j!=i:
                temp_nbr.append(j)
        nodes_nbr[tuple(i)] = temp_nbr
        del temp_nbr
    return nodes_nbr

#function to generate nodes
def generateNode():
    i=0
    while i<N:
        tempNode1 = rnd.randint(0,D)
        tempNode2 = rnd.randint(0,D)
        tempNodes = []
        tempNodes.append(tempNode1)
        tempNodes.append(tempNode2)
        if not nodes:
            nodes.append(tempNodes)
            i = i+1
        else:
            if tempNodes not in nodes:
                nodes.append(tempNodes)
                i = i+1

    
#NetworkX graph with only nodes
def generateGraph0(data):
    G = nx.Graph()
    for i in nodes:
        G.add_node(tuple(i),pos=i)
    pos = nx.get_node_attributes(G,'pos')
    nx.draw(G,pos,node_size=8,node_color='g')
    plt.title("WSN with edges to all neighbours: Area {} X {}".format(D,D))
    plt.show()
    return G

#NetworkX graph with only nodes
def generateGrapK(data):
    G = nx.Graph()
    for i in nodes:
        G.add_node(tuple(i),pos=i)
    for key in data:
        nbr = data[tuple(key)]
        K = int(2)
        j=0
        while j<K:
            ch = rnd.choice(nbr)
            j = j+1
            G.add_edge(tuple(ch),tuple(key))
    pos = nx.get_node_attributes(G,'pos')
    nx.draw(G,pos,node_size=8,node_color='g')
    plt.title("WSN with edges to all neighbours: Area {} X {}".format(D,D))
    plt.show()
    return G

def degreeHistogram(G,clr):
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())
    plt.bar(deg, cnt, width=0.80, color=clr)
    plt.title("Degree Histogram")
    plt.ylabel("Count")
    plt.xlabel("Degree")
    plt.show()

  


##########################

#Calling function to generate nodes
generateNode()

#Calling function generate node & neighbour pairs
nodePair  = neighbour()

#Calling function to generate graph
G = generateGrapK(nodePair)

#print(nx.average_shortest_path_length(G))

#calling function to generate degree historgram
degreeHistogram(G,'b')

