#Imported Packages
#import numpy as np
import random as rnd
import matplotlib.pyplot as plt
import networkx as nx
import collections

###### GLOBAL VARIABLES ######
nodes = [] #nodes list 
D = 500 #Max size of WSN deployment area
N = 350#Number of Nodes
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

#function to plot nodes 
def plotNodes():
    x = []
    y = []
    for i in nodes:
        x.append(i[0])
        y.append(i[1])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.plot(x,y,'ro')
    for i,j in zip(x,y):
        ax.annotate('%s)' %j, xy=(i,j), xytext=(30,0), textcoords='offset points')
        ax.annotate('(%s,' %i, xy=(i,j))
    plt.grid()
    plt.show()
    
#function to print nodes and neighbour pair
def printPairs(data):
    for key in data:
        print('{} -> {} \n'.format(key,data[tuple(key)]))
    
#function to generate network from nodePair data
def generateGraph(data):
    G = nx.Graph()
    for i in nodes:
        G.add_node(tuple(i),pos=i)
    for key in data:
        nbr = data[tuple(key)]
        for i in nbr:
            G.add_edge(tuple(i),tuple(key))
    pos = nx.get_node_attributes(G,'pos')
    d = dict(nx.degree(G))
    nx.draw(G,pos,node_size=[v*10 for v in d.values()],node_color='g')
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

def randomFailure(G,K):
    print('********** GRAPH AFTER {} NODES FAILURE *********'.format(K))
    listofnodes = G.nodes()
    randomnodes = rnd.sample(listofnodes,K)
    G.remove_nodes_from(randomnodes)
    pos = nx.get_node_attributes(G,'pos')
    d = dict(nx.degree(G))
    nx.draw(G,pos,node_size=[v*10 for v in d.values()],node_color='r')
    plt.title("WSN with edges to all neighbours: Area {} X {}".format(D,D))
    plt.show()
    degreeHistogram(G,'r')

def prefAttachment(G):
    d = dict(nx.degree(G))
    ds = []
    z = []
    pref = {}
    s = 0
    for i in d.values():
        s = s+i
    for i in d.values():
        ds.append(i/s)
    mi = min(ds)
    ma = max(ds)
    for i in ds:
        z.append((i-mi)/(ma - mi))
    for i,j in zip(z,d.keys()):
        pref[tuple(j)] = i
    return pref
##########################

#Calling function to generate nodes
generateNode()

#Calling function generate node & neighbour pairs
nodePair  = neighbour()

#Calling function to print the pair
#printPairs(nodePair)

#Calling function to generate graph
G = generateGraph(nodePair)

#calling function to generate degree historgram
degreeHistogram(G,'b')

#Random Nodes Failure
randomFailure(G,int(0.2*D)) #Making 10% of the nodes to fail

prefAttachment(G)
#Plot the graph
#plotNodes()
