import sys
import re
import time

graphRE=re.compile("(\\d+)\\s(\\d+)")
edgeRE=re.compile("(\\d+)\\s(\\d+)\\s(-?\\d+)")

vertices=[]
edges=[]

def BellmanFord(G):
    pathPairs=[]
    d={}
    
    #Initial the graph
    for i in G[0]:
        for j in G[0]:
            d[j]=float('inf')
        d[i]=0
        
        #Logic part(adapting loop)
        for x in range(len(G[0])-1):
            for y in G[0]:
                for z in range(len(G[1])):
                    if float(d[y])+float(G[1][y][z])<float(d[z]):
                        d[z]=float(d[y])+float(G[1][y][z])
    #Check for negative edge                  
        for x in G[0]:
            for y in range(len(G[1])):
                if float(d[x])+float(G[1][x][y])<float(d[y]):
                    print("Negative edge detected.")
                    return false
                
        for k in range(len(d)):
            pathPairs.append(((i,k),float(d[k])))
            
    print("Bellman-Ford:\n"+str(pathPairs))
    return pathPairs

def FloydWarshall(G):
    pathPairs=[]

    #Set all distance to 0
    for i in range(len(vertices)):
        edges[i][i]=0

    #Logic part
    for x in range(len(vertices)):
        for y in range(len(vertices)):
            for z in range(len(vertices)):
                if float(edges[y][x])+float(edges[x][z])<float(edges[y][z]):
                    edges[y][z]=float(edges[y][x])+float(edges[x][z])

    for i in range(len(vertices)):
        for j in range(len(vertices)):
            pathPairs.append(((i,j),float(edges[i][j])))

    print("FloydWarshall:\n"+str(pathPairs))
                
    return pathPairs

def readFile(filename):
    global vertices
    global edges
    # File format:
    # <# vertices> <# edges>
    # <s> <t> <weight>
    # ...
    inFile=open(filename,'r')
    line1=inFile.readline()
    graphMatch=graphRE.match(line1)
    if not graphMatch:
        print(line1+" not properly formatted")
        quit(1)
    vertices=list(range(int(graphMatch.group(1))))
    edges=[]
    for i in range(len(vertices)):
        row=[]
        for j in range(len(vertices)):
            row.append(float("inf"))
        edges.append(row)
    for line in inFile.readlines():
        line = line.strip()
        edgeMatch=edgeRE.match(line)
        if edgeMatch:
            source=edgeMatch.group(1)
            sink=edgeMatch.group(2)
            if int(source) > len(vertices) or int(sink) > len(vertices):
                print("Attempting to insert an edge between "+source+" and "+sink+" in a graph with "+vertices+" vertices")
                quit(1)
            weight=edgeMatch.group(3)
            edges[int(source)-1][int(sink)-1]=weight
    #Debugging
    #for i in G:
        #print(i)
    return (vertices,edges)

def main(filename,algorithm):
    algorithm=algorithm[1:]
    G=readFile(filename)
    # G is a tuple containing a list of the vertices, and a list of the edges
    # in the format ((source,sink),weight)
    if algorithm == 'b' or algorithm == 'B':
        BellmanFord(G)
    if algorithm == 'f' or algorithm == 'F':
        FloydWarshall(G)
    if algorithm == "both":
        start=time.clock()
        BellmanFord(G)
        end=time.clock()
        BFTime=end-start
        start=time.clock()
        FloydWarshall(G)
        end=time.clock()
        FWTime=end-start
        print("Bellman-Ford timing: "+str(BFTime))
        print("Floyd-Warshall timing: "+str(FWTime))

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("python assignment2.py -<f|b> <input_file>")
        quit(1)
    main(sys.argv[2],sys.argv[1])
