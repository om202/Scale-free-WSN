# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 14:19:14 2019

@author: Om
"""

#Imported Packages
#import numpy as np
import random as rnd
import matplotlib.pyplot as plt
import networkx as nx

###### GLOBAL VARIABLES ######
nodes = [] #nodes list 
D = 500 #Max size of WSN deployment area
N = 250#Number of Nodes
R = 50 #Radius of transmission 
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
    for key in data:
        nbr = data[tuple(key)]
        for i in nbr:
            G.add_edge(tuple(key),tuple(i))
    d = nx.degree(G)
    print(d)
    print(nx.clustering(G))
    pos = nx.spring_layout(G)
    nx.draw(G,pos,node_size=6)
    plt.show()
    

##########################

#Calling function to generate nodes
generateNode()

#Calling function generate node & neighbour pairs
nodePair  = neighbour()

#Calling function to print the pair
#printPairs(nodePair)

#Calling function to generate graph
generateGraph(nodePair)

#Plot the graph
plotNodes()
