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
D = 1000 #max size of WSN deployment area
N = 1000 #number of Nodes
R = 250] #Radius of transmission 

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
    plt.show()
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
        permap = perMap(G)
        nbrs_seed = data[tuple(seed)]
        new_permap = {}
        for i in nbrs_seed:
            new_permap[tuple(i)] = permap[tuple(i)]
        flag0 = 0
        for keys in new_permap:
            count0 = 0
            count1 = 0
            if new_permap[keys]==0:
                count0 = count0+1
            else:
                count1 = count1 + 1
            if count0 < count1:
                flag0 = 1
        if flag0==1:
            new_permaprange = perMapRange(new_permap)
            for ij in range(0,3):
                select = rnd.randint(0,100)/100
                for keys in new_permaprange:
                    t = new_permaprange[keys]
                    if select>=t[0] and select<=t[1]:
                        G.add_edge(tuple(seed),keys)
        else:
            G.add_edge(tuple(rnd.choice(nbrs_seed)), tuple(seed))
            #G.add_edge(tuple(rnd.choice(nbrs_seed)), tuple(seed))
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
nx.draw(G,pos,node_size=5,node_color='r')
plt.title("WSN with edges to all neighbours: Area {} X {}".format(D,D))
plt.show()
degreeHistogram(G,'r')


