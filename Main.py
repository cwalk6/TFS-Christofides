import random
import math
from heapq import heapify, heappush, heappop
from collections import deque

#Generating a graph with random locations
def loc_generate(towns):
    townlocs = dict()
    for name in towns:
        reroll = True
        while reroll:
            reroll = False
            x = random.randint(25, 875)
            y = random.randint(25, 875)
            try:
                for towny in townlocs:
                    otherpos = townlocs[towny]
                    if math.sqrt((x-otherpos[0])**2+(y-otherpos[1])**2) < 25:
                        reroll = True
            except:
                continue
        townlocs[name] = (x,y)
    return townlocs

def graph_generate(locations):
    graph = dict()
    for place in locations:
        graph[place] = []
        for other in locations:
            if other == place:
                continue
            estdist = math.sqrt((locations[place][0]-locations[other][0])**2+(locations[place][1]-locations[other][1])**2)
            graph[place].append((other,estdist))
    return graph

def prims_fast(G,s):
    '''Returns mini dist,  graphy = MST'''
    graphy = dict()
    for place in list(G.keys()):
        graphy[place] = []
    explored = {s}
    minimum_count = 0
    #Add all edges from the intial node into the heap and heapify it
    listy = []
    for connections in G[s]:
        listy.append((connections[1], connections[0], s))
    heapify(listy)
    #While loop while len(E) less than length of graph
    while len(explored) < len(G):
        pop = heappop(listy)
        if pop[1] in explored:
            continue
        minimum_count += pop[0]
        explored.add(pop[1])
        graphy[pop[1]].append((pop[2],pop[0]))
        graphy[pop[2]].append((pop[1],pop[0]))
        for connector in G[pop[1]]:
            if connector[0] not in explored:
                heappush(listy,(connector[1], connector[0],pop[1]))
    return minimum_count, graphy

def odd_verts(G):
    '''Checks for odd verticies in a graph and adds them into a set'''
    returnset = set()
    for key in G:
        if len(G[key])%2 != 0:
            returnset.add(key)
    return returnset

def hijkstra(G,s):
    '''return dictionary of lengths of the shortest distance to each node from s length to s is 0'''
    explored = {s}
    dist = {}
    listy = []
    for value in G[s]:
        listy.append((value[1], value[0]))
    heapify(listy)
    while len(explored) < len(G):
        short = heappop(listy)
        if short[1] in explored:
            continue
        explored.add(short[1])
        dist[short[1]] = short[0]
        for edge in G[short[1]]:
            if edge not in explored:
                tuppy = (edge[-1] + dist[short[1]], edge[0])
                heappush(listy,tuppy)
    return dist

def directions(G, s):
    '''Take in graph and starting node to make a path'''
    E = set()
    path = []
    stack = deque([s])
    connectioncheck = set()
    #print(stack)
    while stack:
        explorepoint = stack.pop()
        path.append(explorepoint)
        for node in G[explorepoint]:
            if node not in E:
                if (explorepoint,node[0]) not in connectioncheck and (node[0],explorepoint) not in connectioncheck:
                    stack.append(node[0])
                    connectioncheck.add((explorepoint,node[0]))
                    break
                else:
                    E.add(node[0])
    return path

def add_pairs(og_graphy,mod_graph,modverts):
    '''Takes in an original graph, MST, and verts to find pairs for, adds them, and returns the MST with added pairs'''
    modvertlist = list(modverts)
    while modvertlist:
        name = modvertlist[0]
        dist = hijkstra(og_graphy,name)
        for node in dist:
            if node in modvertlist:
                if node != name:
                    dupe = False
                    for tup in mod_graph[name]:
                        if  tup[0] == node:
                            dupe = True
                    if dupe == False:
                        mod_graph[name].append((node, dist[node]))
                        mod_graph[node].append((name, dist[node]))
                        modvertlist.remove(name)
                        #print(node)
                        #print(modvertlist)
                        modvertlist.remove(node)
                        break

    return mod_graph

def eulerian_cycle(pos_graph,cycle,directions):
    '''Takes in max graph, the cycle graph, and the directions list and finds places to trim it down, returning the graph of a eulerian cycle and the new directions list'''
    E =  set()
    newdirections = []
    for i in range(len(directions)):
        if directions[i] in E:
            if i == len(directions)-1:
                newdirections.append(directions[i])
                break
            else:
                pair = (directions[i-1],directions[i+1])
                backwards = pos_graph[directions[i-1]]
                forwards = pos_graph[directions[i+1]]
                for node in cycle[directions[i]]:
                    if node[0] == backwards:
                        cycle[pair[0]].remove((directions[i],node[1]))
                        cycle[directions[i]].remove((pair[0],node[1]))
                    if node[0] == forwards:
                        cycle[pair[1]].remove((directions[i],node[1]))
                        cycle[directions[i]].remove((pair[1],node[1]))
                dist = math.sqrt((backwards[0]-forwards[0])**2+(backwards[1]-forwards[1])**2)
                cycle[pair[0]].append((pair[1],dist))
                cycle[pair[1]].append((pair[0],dist))
        else:
            newdirections.append(directions[i])
        E.add(directions[i])

    return cycle, newdirections


#Beginning code
towns1 = ["House", "Cabin", "Cave", "Mushroom", "Treehouse"]
cords = loc_generate(towns1)
originalgraph = graph_generate(cords)
cuesta, graph = prims_fast(originalgraph,"House")
modifyverts = odd_verts(graph)
graph = add_pairs(originalgraph,graph,modifyverts)
chart = directions(graph,"House")
print(eulerian_cycle(cords,graph,chart))