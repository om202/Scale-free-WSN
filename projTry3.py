#Imported Packages
#import numpy as np
import random as rnd
import matplotlib.pyplot as plt
import networkx as nx
import collections
import operator

###### GLOBAL VARIABLES ######
nodes = [] #nodes list 
D = 500 #max size of WSN deployment area
N = 200#Number of Nodes
R = 100 #Radius of transmission 
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
        K = int(0.3*len(nbr))
        j=0
        while j<K:
            ch = rnd.choice(nbr)
            j = j+1
            G.add_edge(tuple(ch),tuple(key))
    #pos = nx.get_node_attributes(G,'pos')
    #nx.draw(G,pos,node_size=8,node_color='g')
    #plt.title("WSN with edges to all neighbours: Area {} X {}".format(D,D))
    #plt.show()
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

 
    #-----------------------------------

#probability of each node's degree
#in resepect to WHOLE NETWORK
def perMap(G):
    per = []
    permap = {}
    temp = nx.degree(G)
    sum = 0
    for i in temp:
        sum = sum + i[1]
    for i in temp:
        per.append(i[1]/sum)
    for i,j in zip(temp,per):
        permap[i[0]]=j
    return permap

#ROULETTE METHOD
def perMapRange(permap):
    #first mapping permap to [0,1]
    permap_mapped = {}
    _sum = 0.0
    for keys in permap:
        _sum = _sum + permap[keys]
    for keys in permap:
        permap_mapped[keys] = permap[keys]/_sum
    #finding out ranges     
    permaprange = {}
    prev = 0.0
    sorted_permap = dict(sorted(permap_mapped.items(), key=operator.itemgetter(1)))
    for keys in sorted_permap:
        t = []
        new = sorted_permap[keys]
        margin = 0.00001
        a = prev
        b = new+prev-margin
        if a==0.0 and b==-margin:
            t.append(0.0)
            t.append(0.0)
        else:
            t.append(a)
            t.append(new+prev-margin)
        permaprange[keys] = tuple(t)
        prev = new+prev
        del t        
    return permaprange

def prefAttachment(G):
    permap = perMap(G)
    #print('Permap: {}'.format(permap))
    permaprange = perMapRange(permap)
    #print('\nPermarange: {}'.format(permaprange))
    #G.add_node('NEW')
    #randInt to select a node from permarange
    select = rnd.randint(0,100)/100
    #print('\n\nselect probability: {}'.format(select))
    for keys in permaprange:
        t = permaprange[keys]
        if select>=t[0] and select<=t[1]:
            #print('Node Choosed: {}'.format(keys))
            G.add_edge(rnd.randint(0,200),keys)
    
    
    #--------------------------------------


##########################

#Calling function to generate nodes
generateNode()

#Calling function generate node & neighbour pairs
nodePair  = neighbour()

#Calling function to generate graph
G = generateGrapK(nodePair)

#----------------------

for i in range(0,200):
    prefAttachment(G)


d = dict(nx.degree(G))
pos = nx.random_layout(G)
nx.draw(G,pos,node_size=[v*10 for v in d.values()],node_color='y')
plt.show()
degreeHistogram(G,'r')

#-----------------------

#print(nx.average_shortest_path_length(G))

#calling function to generate degree historgram
degreeHistogram(G,'b')

