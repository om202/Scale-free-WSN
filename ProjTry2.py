import networkx as nx
import operator
import matplotlib.pyplot as plt
import random as rnd
import collections

#ls = [1,2,3,4]
ls = []

k=10

for i in range(1,k):
    ls.append(i)

Gr = nx.Graph()
Gr.add_nodes_from(ls)


for i in range(0,int(k*2)):
    j = rnd.choice(ls)
    k = rnd.choice(ls)
    Gr.add_edge(j,k)

#Gr.add_edge(2,3)

'''
G.add_edge(1,2)
#G.add_edge(1,3)
G.add_edge(2,3)
G.add_edge(2,4)
G.add_edge(2,10)
G.add_edge(1,9)
G.add_edge(4,8)
G.add_edge(6,1)
G.add_edge(6,10)
G.add_edge(5,2)
'''

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
    G.add_node('NEW')
    #randInt to select a node from permarange
    select = rnd.randint(0,100)/100
    print('\n\nselect probability: {}'.format(select))
    for keys in permaprange:
        t = permaprange[keys]
        if select>=t[0] and select<=t[1]:
            print('Node Choosed: {}, Its degree: {}'.format(keys,G.degree(int(keys))))
            #G.add_edge(rnd.randint(0,10),keys)
            G.add_edge('NEW',keys)
    
for i in range(0,int(k*5)):
    prefAttachment(Gr)

d = dict(nx.degree(Gr))
pos = nx.circular_layout(Gr)
nx.draw(Gr,pos,node_size=[v*100 for v in d.values()],node_color='y', with_labels=True)
plt.show()
degreeHistogram(Gr,'r')