from PIL import Image
from Queue import PriorityQueue as pq
import time


class RPQ(pq):

	def put(self, tup):
		newtup = tup[0] * -1, tup[1], tup[2]
		pq.put(self, newtup)
	
	def get(self):
		tup = pq.get(self)
		newtup = tup[0] * -1, tup[1], tup[2]
		return newtup


class ANAPlanner(object):
	
	def __init__(self, map, start, goal):
		super(ANAPlanner, self).__init__()
		self.map = map
		self.map = self.map.convert('1')
		self.size = self.map.size
		self.map = self.map.load()
		self.start = start
		self.goal = goal
		
		self.G = 1e15 
		self.E = 1e15 


		self.open = RPQ(0) 
		self.predessor = {}
		self.expanded = {}
		self.frontier = {}

		self.stats = {}

	def ana_star(self):

		sub_count = 0
		
		h_start = self.heuristic(self.start, self.goal)
		e = self.compute_e(self.G, 0, h_start)

		self.open.put((e, 0, self.start))


		self.predessor[self.start] = None
		self.expanded[self.start] = 0
				
		while not self.open.empty():
			sub_count += 1
			t1 = time.time()
			self.improve_solution()
			t2 = time.time()
			dt = t2 - t1
			
			self.stats[sub_count] = [self.G,self.E,dt]
			self.prune()
			
		self.path = []
		current_node = self.goal
		while current_node != self.start:
			self.path.append(current_node)
			current_node = self.predessor[current_node]
		self.path.append(self.start)
		self.path.reverse()	

		for f in self.open.queue:
			self.frontier[f[2]] = f[1]


	def improve_solution(self):
		
		while not self.open.empty():
			current_node = self.open.get()
			e_s = current_node[0]
			g_s = current_node[1]
			state = current_node[2]
			
			if e_s < self.E:
				self.E = e_s

			if state == self.goal:
				self.G = g_s
				break

			for suc in self.expand_nodes(state):
				new_cost = self.expanded[state] + 1
				if suc not in self.expanded or new_cost < self.expanded[suc] :
					self.expanded[suc] = new_cost
					h_child = self.heuristic(self.goal, suc)
					total_cost = new_cost + h_child
					if total_cost < self.G:
						e_suc = self.compute_e(self.G, new_cost, h_child)
						self.open.put((e_suc, new_cost, suc))
					self.predessor[suc] = state

	def heuristic(self,a, b):
		(x1, y1) = a
		(x2, y2) = b
		h = abs(x2 - x1) + abs(y2 - y1) # Manhattan Distance
		return h

	def compute_e(self,G, g, h):
		e = (G - g)/(h + 1e-15)
		return e

	def expand_nodes(self, node):
		x = node[0]
		y = node[1]
		results = []

		x_max = self.size[0]
		y_max = self.size[1]

		if (x+1 < x_max) and (self.map[x+1,y] != (255-self.map[self.start[0],self.start[1]])): #1
			results.append((x+1,y)) 

		if (y+1 < y_max) and (self.map[x,y+1] != (255-self.map[self.start[0],self.start[1]])): #1
			results.append((x,y+1))

		if (y>=1) and self.map[x,y-1] != (255-self.map[self.start[0],self.start[1]]): #1
			results.append((x,y-1))

		if (x>=1) and self.map[x-1,y] != (255-self.map[self.start[0],self.start[1]]): #1
			results.append((x-1,y))

		return results

	 
	def prune(self):
		update = RPQ(0)

		while not self.open.empty():
			node = self.open.get()
			e_s = node[0]
			g_s = node[1]
			state = node[2]

			h_s = self.heuristic(state, self.goal)

			if g_s + h_s < self.G:
				new_e_s = self.compute_e(self.G, g_s, h_s)
				update.put((new_e_s, g_s, state))
			
		self.open = update
