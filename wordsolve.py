import pickle
import networkx as nx
keepgoing=True


def buildDict(l,name):
    f=open("Downloads/wordsEn.txt","r")
    llist4=[]
    d={}
    for line in f:
        if len(line)==l+1:
            llist4.append(line.replace("\n",""))


    for word in llist4:
        
        l=[]
        for i in range(len(word)):
            for j in range(26):
                lw=list(word)
                lw[i]=chr(97+j)
                w=''.join(lw)
                if w in llist4 and (w != word):
                    l.append(w)
                    try:
                        if word not in d[w]:
                            d[w]=d[w]+[word]
                    except:
                        pass
        d[word]=l

    print d
    p=open(name,"w")
    pickle.dump(d, p)
    p.close()
    f.close()


def bfs(dictname, start, end):
    global keepgoing
    f=open(dictname, "r")
    d=pickle.load(f)
    f.close()
    x=[[start, d[start], [start]]]
    while keepgoing==True:
        x=step(x, end, d)


def step(listnodes, end, d): #need to store path somehow
    global keepgoing
    #[[node, connections, path to node]]
    newlist=[]
    for item in listnodes:
        if item[0]==end:
            keepgoing=False
            print str(item[2])
        else:
            for x in item[1]:
                try:
                    ld=d[x]
                    ld.remove(item[0])
                except:
                    ld=[]
                newlist.append([x,ld,item[2]+[x]])

    allempty=True
    for item in newlist:
        if item[0]!=[]:
            allempty=False
            break
    if allempty==True:
        print "No route found"
        keepgoing=False

    return newlist

def plotnetwork(name):
    f=open(name, "r")
    d=pickle.load(f)
    f.close()
    graph=nx.Graph()
    for item in d.keys():
        graph.add_node(item)
        for element in d[item]:
            graph.add_edge(item, element)
    nx.write_gml(graph, "testw.gml")


    
#buildDict(6,"wdict6.pkl")
bfs("wdict6.pkl", "bucket", "butler")
#plotnetwork("wdict6.pkl")
