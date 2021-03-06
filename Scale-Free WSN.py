#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 17:47:48 2019

@author: omprakash
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 11:09:43 2019

@author: omprakash
"""

#Imported Packages
#import numpy as np
import random as rnd
import matplotlib.pyplot as plt
import networkx as nx
import collections
import operator
import powerlaw

nodes = [] #nodes list 
D = 1000 #max size of WSN deployment area
N = 1000 #number of Nodes
R =  200 #Radius of transmission 
HD = 100 #highest degree
PTE = 0.01 #percentage of total edges 
#RB = 0.04 #Random break of nodes 
m = 1 #links with each new node

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

def randomBreak_v1(G,RB):
    GC = G.copy()
    nodes = list(GC.nodes())
    i = 0
    while i<RB:
        x = tuple(rnd.choice(nodes)) 
        GC.remove_node(x)
        nodes.remove(x)
        i = i + 1
    #print('Number of nodes removed: {}'.format(i))
    return GC

def randomBreak_v2(GC,RB):
    nodes = list(GC.nodes())
    i = 0
    while i<RB:
        x = tuple(rnd.choice(nodes)) 
        GC.remove_node(x)
        nodes.remove(x)
        i = i + 1
    #print('Number of nodes removed: {}'.format(i))
    return GC

def degreeLoglog(G,clr):
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())
    #plt.bar(deg, cnt, width=0.80, color=clr)
    plt.loglog(deg,cnt,'bo')
    plt.title("Degree Histogram")
    plt.ylabel("Count")
    plt.xlabel("Degree")
    plt.show()

def degreeHistogram(G,clr):
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())
    plt.bar(deg, cnt, width=0.80, color=clr)
    #plt.loglog(deg,cnt)
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
        if i[1] < HD:
            per.append(i[1]/sum)
        else:
            per.append(i[1]/(sum*i[1]))
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
    for ii in range(0,int(((N*(N-1))/2)*PTE)):
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

        _sum = 0
        for keys in permap_mapped:
            _sum = _sum + permap_mapped[keys]
        
        if _sum == 0:
            for jj in range(0,m):
                rnd_nbr = tuple(rnd.choice(nbrs_seed))
                G.add_edge(rnd_nbr, tuple(seed))
            #print('Seed: {} --> rnd_nbr: {} \n'.format(seed,rnd_nbr))
        else:
            new_permaprange = perMapRange(permap_mapped)
            for jj in range(0,m):
                select = rnd.uniform(0,1)
                for keys in new_permaprange:
                    t = new_permaprange[keys]
                    if select>=t[0] and select<=t[1]:
                        #print('Seed: {} --> Key: {} \n'.format(seed,keys))
                        G.add_edge(tuple(seed),keys)

        seed = rnd.choice(nbrs_seed)
    
    #Rewire
    final_degree = nx.degree(G)
    final_0nodes = []
    for keys in final_degree:
        if keys[1] == 0:
            final_0nodes.append(keys[0])
    for i in final_0nodes:
        nbr_i = data[tuple(i)]
        flag = 0
        while flag!=1:
            rnd_nbr_i = tuple(rnd.choice(nbr_i))
            if G.degree(rnd_nbr_i)!=0:
                G.add_edge(rnd_nbr_i,tuple(i))
                flag = 1  
    
    permap = perMap(G) #prob map of each node wrt whole graph
    #print(permap)
    return G

def findHubs(d):
    deg = []
    for i in d:
        deg.append(d[i])
    
    deg.sort()
    
    h = []
    for i in deg:
        if i>(deg[-1]/2):
            h.append(i)
    
    hub = []
    for i in h:
        for j in d:
            if i == d[j]:
                hub.append(j)
    return hub

def showGraph(G):
    d=dict(nx.degree(G))

    hub = findHubs(d)
    
    node_color = []
    for node in G:
        if node in hub:
            node_color.append('red')
        else:
            node_color.append('brown')
    
    
    pos = nx.get_node_attributes(G,'pos')
    nx.draw(G,pos,node_size=[v*10 for v in d.values()],node_color=node_color)
    plt.title("Scale Free WSN: Area {} X {}, Nodes: {}".format(D,D,N))
    plt.ylabel('Hubs: Red, Other: Brown')
    plt.show()
    
def powerlaw_gamma(g):
    degrees = {}
    
    nodes = list(g.node)
    
    for node in nodes:
        key = len(list(g.neighbors(node)))
        degrees[key] = degrees.get(key, 0) + 1
    
    max_degree = max(degrees.keys(), key=int)
    num_nodes = []
    for i in range(1, max_degree + 1):
        num_nodes.append(degrees.get(i, 0))
    
    fit = powerlaw.Fit(num_nodes)
    #fit.power_law.plot_pdf( color= 'b',linestyle='--',label='fit ccdf')
    #fit.plot_pdf( color= 'b', linestyle='-');
    print(fit.power_law.alpha)
    

##########################
generateNode() #Calling function to generate nodes
nodePair  = neighbour() #Calling function generate node & neighbour pairs
G = generateGraph0() #Calling function to generate graph

#Choosing a center element
pos = nx.get_node_attributes(G,'pos')
r1 = D*0.35
r2 = D*0.55
center = []
for keys in pos:
    if keys[0]>r1 and keys[0]<r2 and keys[1]>r1 and keys[1]<r2:
        center.append(keys)
seed = rnd.choice(center)

G = prefAttachment(G,seed,nodePair)

showGraph(G)

degreeHistogram(G,'brown')
degreeLoglog(G,'g')
#print(nx.average_shortest_path_length(G))
powerlaw_gamma(G)

#Robustness Analysis
t= 0
min_nmcc = 1000000000000
for t in range(0,1):
    GC = G.copy()
    breaks = 0
    nodes_mcc = 2
    worst_case_nmcc = []
    worst_case_br = []
    br = []
    nmcc = []
    while breaks<=N and nodes_mcc>1:
        Gd = randomBreak_v2(GC,1)
        MCC = max(nx.connected_component_subgraphs(Gd), key=len)
        nodes_mcc = len(MCC)
        breaks = breaks + 1
        br.append(breaks)
        nmcc.append(nodes_mcc)
    
    #Expanding
    br.append(N)
    nmcc.append(1)
    
    if sum(nmcc) < min_nmcc:
        min_nmcc = sum(nmcc)
        worst_case_nmcc = nmcc
        worst_case_br = br
        
    diag = []
    d = 0
    while d<=N:
        diag.append(d)
        d = d + 1 

plt.plot(worst_case_br,worst_case_nmcc,'b')
diag_rev = diag.copy()
diag_rev.reverse()
plt.plot(diag,diag_rev,'y')

plt.title('Robustness of Algorithm')
plt.xlabel('Number of Random Breaks')
plt.ylabel('Number of nodes in MCC')
plt.show()   
