import sys
from PIL import Image
import copy

from Queue import PriorityQueue
import time

'''
These variables are determined at runtime and should not be changed or mutated by you
'''
start = (0, 0)  # a single (x,y) tuple, representing the start position of the search algorithm
end = (0, 0)    # a single (x,y) tuple, representing the end position of the search algorithm
difficulty = "" # a string reference to the original import file

'''
These variables determine display color, and can be changed by you, I guess
'''

PURPLE = (85, 26, 139)
LIGHT_GRAY = (50, 50, 50)
DARK_GRAY = (100, 100, 100)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

stats = []

'''
These variables are determined and filled algorithmically, and are expected (and required) be mutated by you
'''
path = []       # an ordered list of (x,y) tuples, representing the path to traverse from start-->goal
expanded = {}   # a dictionary of (x,y) tuples, representing nodes that have been expanded
frontier = {}   # a dictionary of (x,y) tuples, representing nodes to expand to in the future


def heuristic(a, b):
	(x1, y1) = a
	(x2, y2) = b
	h = abs(x2 - x1) + abs(y2 - y1) # Manhattan Distance
	return h

def expand_nodes(map, size, node):
	x = node[0]
	y = node[1]
	results = []

	x_max = size[0]
	y_max = size[1]
	

	if (x+1 < x_max) and (map[x+1,y] != 0): #1
		results.append((x+1,y))

	if (y+1 < y_max) and (map[x,y+1] != 0): #1
		results.append((x,y+1))

	if (y>=1) and map[x,y-1] != 0: #1
		results.append((x,y-1))

	if (x>=1) and map[x-1,y] != 0: #1
		results.append((x-1,y))

	return results
	
def A_star(map, size, start, goal):
	front = PriorityQueue(0)
	front.put((0, start))
	parent_linked = {}
	explored = {}

	parent_linked[start] = None
	explored[start] = 0
	G = 0
	while front.qsize():
		current_node = front.get()[1]

		if current_node == goal:
			G = front.get()[0]
			break

		for child_node in expand_nodes(map, size, current_node):
			new_cost = explored[current_node] + 1
			if child_node not in explored or new_cost < explored[child_node] :
				explored[child_node] = new_cost
				total_cost = new_cost + heuristic(goal, child_node)
				front.put((total_cost, child_node))
				parent_linked[child_node] = current_node

	path = []
	while current_node != start:
		path.append(current_node)
		current_node = parent_linked[current_node]
	path.append(start)
	path.reverse()
   
	frontier = {}
	for f in front.queue:
		frontier[f[1]] = f[0]

	return path, explored, frontier, G


def search(map, size, output_name):

	global path, start, end, path, expanded, frontier, stats
	
	"""
	This function is meant to use the global variables [start, end, path, expanded, frontier] to search through the
	provided map.
	:param map: A '1-concept' PIL PixelAccess object to be searched. (basically a 2d boolean array)
	"""
	print ("")
	print "Start Point: " + str(start)
	print "End   Point: " + str(end)

	# O is unoccupied (white); 1 is occupied (black)
	print ("")
	print "pixel value at start point ", map[start[0], start[1]]
	print "pixel value at end point ", map[end[0], end[1]]

	start_time = time.time()
	path, expanded, frontier, G = A_star(map, size, start, end)
	end_time = time.time()
	time_diff = end_time - start_time

	print("")
	print("Cost G:     ") + str(G) + ' units'
	print("Time Taken: ") + str(time_diff) + ' sec'

	stats.append(G)
	stats.append(time_diff)
	
	# print stats
	visualize_search(output_name) # see what your search has wrought (and maybe save your results)

def visualize_search(save_file="do_not_save.png"):
	"""
	:param save_file: (optional) filename to save image to (no filename given means no save file)
	"""
	im = Image.open(difficulty).convert("RGB")
	pixel_access = im.load()

	# draw start and end pixels
	pixel_access[start[0], start[1]] = GREEN
	pixel_access[end[0], end[1]] = GREEN

	# draw expanded pixels
	for pixel in expanded.keys():
		pixel_access[pixel[0], pixel[1]] = LIGHT_GRAY

	# draw path pixels
	for pixel in path:
		pixel_access[pixel[0], pixel[1]] = GREEN

	 # draw frontier pixels
	for pixel in frontier.keys():
		pixel_access[pixel[0], pixel[1]] = RED
	
	# display and (maybe) save results
	# im.show()
	if(save_file != "do_not_save.png"):
		im.save(save_file)
	im.close()

if __name__ == "__main__":
	# Throw Errors && Such
	assert sys.version_info[0] == 2                                 # require python 2 (instead of python 3)
	assert len(sys.argv) == 2, "Incorrect Number of arguments"      # require difficulty input
	# Parse input arguments
	function_name = str(sys.argv[0])
	difficulty = str(sys.argv[1])
	print ("")
	print ("A* Implementation")
	print "running " + function_name + " with " + difficulty + " difficulty."

	# Hard code start and end positions of search for each difficulty level
	if difficulty == "trivial.gif":
		start = (8, 1)
		end = (20, 1)
	elif difficulty == "medium.gif":
		start = (8, 201)
		end = (110, 1)
	elif difficulty == "hard.gif":
		start = (10, 1)
		end = (401, 220)
	elif difficulty == "very_hard.gif":
		start = (1, 324)
		end = (580, 1)
	elif difficulty == "3.png":
		start = (0,0)
		end = (479,479)
	elif difficulty == "2.png":
		start = (0,0)
		end = (479,479)
	elif difficulty == "7.jpg":
		start = (817,279)
		end = (243,187)
	else:
		start = (5,5)
		end = (1150, 640)
		#assert False, "Incorrect difficulty level provided"

	# Perform search on given image
	im = Image.open(difficulty)
	fil = open(difficulty[:-4]+"_stats_astar.txt",'a')
	im = im.convert('1')
	search(im.load(), im.size,difficulty[:-4]+"_astar.png")
	# print stats
	fil.write(str(stats[0])+"|"+str(stats[1])+"|\n")
