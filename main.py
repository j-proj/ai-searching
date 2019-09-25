import queue
import copy
import time

class Graph:
    def __init__(self):
        self.graph = dict()      # store adj list as graph
        self.visited = dict()    # store visited list
        self.heuristic = dict()  # store heuristic weight

    def addnodes(self, node1, node2, weight):
        node1 = node1
        node2 = node2
        if node1 not in self.graph:
            self.graph[node1] = {}
        self.graph[node1][node2] = float(weight)
        if node2 not in self.graph:
            self.graph[node2] = {}
        self.graph[node2][node1] = float(weight)
        self.visited[node1] = False
        self.visited[node2] = False

    def addheuristic(self, node, heuristic):
        self.heuristic[node] = float(heuristic)

    def print(self):
        for u in self.graph:
            for v in self.graph[u]:
                print(u, " ", v, " weight: ", self.graph[u][v])

    def bfs(self, start, end):
        start = start
        end = end
        parentdict = dict()
        visitcount = 0
        distance = 0.0
        pathcount = 0
        visited = copy.deepcopy(self.visited)
        visited[start] = True
#       create queue to add vertices in order of visit
        queue = []
        queue.append(start)
        while queue:
            visitcount += 1
            curr = queue.pop(0)

#           if the current vertex is not the ending node
#           visit the children and add them to the queue
            if curr != end:
                for u in self.graph[curr]:
                    if visited[u] is False:
                        visited[u] = True
                        queue.append(u)         # add child to queue
                        parentdict[u] = curr

#           if the current vertex is the ending node, print
#           # of nodes visited and on path, and distance
            if curr == end:
                print("bfs")
                print("Num nodes visited: ", visitcount)
                while curr in parentdict:
                    distance += self.graph[parentdict[curr]][curr]
                    curr = parentdict[curr]
                    pathcount += 1
                print("Num nodes on path: ", pathcount + 1)
                print("Distance(km): ", distance)
                print(" ")
                return

    def ucs(self, start, end):
        parentdict = dict()
        pathcount = 0
        distance = dict()
        visited = copy.deepcopy(self.visited)
        visitcount = 0
        q = queue.PriorityQueue()       # use priority queue so visit by distance weight

        q.put((0, start))
        visited[start] = True
        while q is not q.empty():
            visitcount += 1
            temp = q.get()
            curr = temp[1]
            distance[curr] = temp[0]
            if curr != end:
                for u in self.graph[curr]:
                    if u in distance:       # if true, been visited before
                        cost = self.graph[u][curr] + distance[curr]
                        if cost < distance[u]:          # if the new cost is smaller
                            distance[u] = cost          # choose this path over previous
                            parentdict[u] = curr
                            q.put((distance[u], u))
                    else:
                        distance[u] = self.graph[u][curr] + distance[curr]
                        parentdict[u] = curr
                        q.put((distance[u], u))

            if curr == end:
                print("ucs")
                print("Num nodes visited: ", visitcount)
                while curr in parentdict:
                    curr = parentdict[curr]
                    pathcount += 1
                print("Num nodes on path: ", pathcount + 1)
                print("Distance(km): ", distance[end])
                print(" ")
                return

# mostly the same as the uniform cost search, just adding heuristic to the cost
# heuristic is the euclidean distance from node to node
    def astar(self, start, end):
        parentdict = dict()
        distance = dict()
        pathcount = 0
        visited = copy.deepcopy(self.visited)
        visitcount = 0
        q = queue.PriorityQueue()

        q.put((self.heuristic[start], start))
        visited[start] = True
        while q is not q.empty():
            visitcount += 1
            temp = q.get()
            curr = temp[1]
            distance[curr] = temp[0] - self.heuristic[curr]
            if curr != end:
                for u in self.graph[curr]:
                    if u in distance:
                        cost = self.graph[u][curr] + distance[curr] + self.heuristic[u]
                        if cost < distance[u]:
                            distance[u] = cost
                            parentdict[u] = curr
                            q.put((distance[u], u))
                    else:
                        distance[u] = self.graph[u][curr] + distance[curr] + self.heuristic[u]
                        parentdict[u] = curr
                        q.put((distance[u], u))
            if curr == end:
                print("astar")
                print("Num nodes visited: ", visitcount)
                while curr in parentdict:
                    curr = parentdict[curr]
                    pathcount += 1
                print("Num nodes on path: ", pathcount + 1)
                print("Distance(km): ", distance[end])
                print(" ")
                return


temp = Graph()
with open("edges.txt", 'r') as file:
    for line in file:
        strs = line.split()
        temp.addnodes(strs[0],strs[1], strs[2])

with open("heuristic.txt", 'r') as file:
    for line in file:
        strs = line.split()
        temp.addheuristic(strs[0], strs[1])


temp.bfs('107560551', '105012740')
temp.ucs('107560551', '105012740')
temp.astar('107560551', '105012740')
