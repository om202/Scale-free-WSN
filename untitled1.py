#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 11:13:54 2019

@author: omprakash
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 16:15:51 2019

@author: omprakash
"""

#Imported Packages
#import numpy as np
import random as rnd
import matplotlib.pyplot as plt
import networkx as nx
import collections
import operator

nodes = [] #nodes list 
D = 500 #max size of WSN deployment area
N = 500 #number of Nodes
R = 150 #Radius of transmission 

#function to sort values in the nodes
def sorti(n):
    return(sorted(nodes,key=lambda x:x[0])) #sorting via 'x'
 
#Function to find distance between two nodes
def distance(i,j):
    x = abs(i[0]-j[0])
    y = abs(i[1]-j[1])
    d = (x**2 + y**2)**(1/2)
    return d    

#Function to identify neighbours of each nodes
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

#function to generate node pairs
def generateNode():
    i=0
    while i<N:
        tempNode1 = rnd.randint(0,D)
        tempNode2 = rnd.randint(0,D)
        tempNodes = []
        tempNodes.append(tempNode1)
        tempNodes.append(tempNode2)
        if tempNodes not in nodes:
            nodes.append(tempNodes)
            i = i+1
    
#NetworkX graph with only nodes (without any edges)
def generateGraph0():
    G = nx.Graph()
    for i in nodes:
        G.add_node(tuple(i),pos=i)
    pos = nx.get_node_attributes(G,'pos')
    nx.draw(G,pos,node_size=8,node_color='g')
    plt.title("WSN with edges to all neighbours: Area {} X {}".format(D,D))
    #plt.show()
    return G

def generateGraphRand():
    G = nx.Graph()
    for i in nodes:
        G.add_node(tuple(i),pos=i)
    j=0
    while(j<int(0.5*N)):
        a = tuple(rnd.choice(nodes))
        b = tuple(rnd.choice(nodes))
        G.add_edge(a,b)
        j = j+1
    '''pos = nx.get_node_attributes(G,'pos')
    nx.draw(G,pos,node_size=8,node_color='g')
    plt.title("WSN with edges to all neighbours: Area {} X {}".format(D,D))
    plt.show()'''
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

#probability of each node's degree
#in resepect to WHOLE NETWORK
def perMap(G):
    per = []
    permap = {}
    temp = nx.degree(G)
    sum = 0
    for i in temp:
        sum = sum + i[1]
    if sum == 0:
        sum = 0.000000001
    for i in temp:
        per.append(i[1]/sum)
    for i,j in zip(temp,per):
        permap[i[0]]=j
    return permap

#ROULETTE METHOD
def perMapRange(permap):
    #finding out ranges     
    permaprange = {}
    prev = 0.0
    sorted_permap = dict(sorted(permap.items(), key=operator.itemgetter(1)))
    for keys in sorted_permap:
        t = []
        new = sorted_permap[keys]
        margin = 0.00001
        a = prev
        b = new+prev-margin
        if a == 0 and b < 0:
            t.append(0)
            t.append(0)
        else:
            t.append(a)
            t.append(b)
        permaprange[keys] = tuple(t)
        prev = new+prev
        del t   
    #print(permaprange)
    return permaprange

def prefAttachment(G,seed,data):   
    for ii in range(0,D):
        permap = perMap(G) #prob map of each node wrt whole graph
        nbrs_seed = data[tuple(seed)] #nbrs of the seed node
        new_permap = {}
        for i in nbrs_seed:
            new_permap[tuple(i)] = permap[tuple(i)]
            
        #first mapping permap to [0,1]
        permap_mapped = {}
        _sum = 0.0
        for keys in new_permap:
            _sum = _sum + new_permap[keys]
        if _sum == 0:
            _sum = 0.0000001
        for keys in new_permap:
            permap_mapped[keys] = (new_permap[keys]/_sum)
        
        count0 = 0
        keys_0 = []
        count1 = 0
        for keys in permap_mapped:
            if permap_mapped[keys]==0:
                count0 = count0+1
                keys_0.append(keys)
            else:
                count1 = count1 + 1
        
        #print('count0 {} count1 {}'.format(count0,count1))
        
        if count1>count0:
            new_permaprange = perMapRange(permap_mapped)
            #print(new_permaprange)
            select = rnd.uniform(0,1)
            for keys in new_permaprange:
                t = new_permaprange[keys]
                if select>=t[0] and select<=t[1]:
                    print('Seed: {} --> Key: {} \n'.format(seed,keys))
                    G.add_edge(tuple(seed),keys)
        else:
            rnd_nbr = tuple(rnd.choice(keys_0))
            G.add_edge(rnd_nbr, tuple(seed))
            print('Seed: {} --> rnd_nbr: {} \n'.format(seed,rnd_nbr))
            #print('EXEC')
        seed = rnd.choice(nbrs_seed)
    return G

##########################
generateNode() #Calling function to generate nodes
nodePair  = neighbour() #Calling function generate node & neighbour pairs
G = generateGraph0() #Calling function to generate graph

#Choosing a center element
pos = nx.get_node_attributes(G,'pos')
r1 = D*0.4
r2 = D*0.5
center = []
for keys in pos:
    if keys[0]>r1 and keys[0]<r2 and keys[1]>r1 and keys[1]<r2:
        center.append(keys)
seed = rnd.choice(center)

G = prefAttachment(G,seed,nodePair)

d=dict(nx.degree(G))
pos = nx.get_node_attributes(G,'pos')
nx.draw(G,pos,node_size=2,node_color='r',with_labels=True)
plt.title("WSN with edges to all neighbours: Area {} X {}".format(D,D))
plt.show()
degreeHistogram(G,'r')

#print(nx.average_shortest_path_length(G))


