import sys
from PIL import Image
import copy
import numpy as np 
import time 


from anastar import *

'''
These variables are determined at runtime and should not be changed or mutated by you
'''
start = (0, 0)  # a single (x,y) tuple, representing the start position of the search algorithm
end = (0, 0)    # a single (x,y) tuple, representing the end position of the search algorithm
difficulty = "" # a string reference to the original import file

'''
These variables determine display coler, and can be changed by you, I guess
'''
NEON_GREEN = (0, 255, 0)
PURPLE = (85, 26, 139)
LIGHT_GRAY = (50, 50, 50)
DARK_GRAY = (100, 100, 100)

'''
These variables are determined and filled algorithmically, and are expected (and required) be mutated by you
'''
path = []       # an ordered list of (x,y) tuples, representing the path to traverse from start-->goal
expanded = {}   # a dictionary of (x,y) tuples, representing nodes that have been expanded
frontier = {}   # a dictionary of (x,y) tuples, representing nodes to expand to in the future

def Search(map,output_name,filename):
	"""
	This function is meant to use the global variables [start, end, path, expanded, frontier] to search through the
	provided map.
	:param map: A '1-concept' PIL PixelAccess object to be searched. (basically a 2d boolean array)
	# """

	# O is unoccupied (white); 1 is occupied (black)
	print "pixel value at start point ", map[start[0], start[1]]
	print "pixel value at end point ", map[end[0], end[1]]

	# put your final path into this array (so visualize_search can draw it in purple)
	path.extend([(8,2), (8,3), (8,4), (8,5), (8,6), (8,7)])

	# put your expanded nodes into this dictionary (so visualize_search can draw them in dark gray)
	expanded.update({(7,2):True, (7,3):True, (7,4):True, (7,5):True, (7,6):True, (7,7):True})

	# put your frontier nodes into this dictionary (so visualize_search can draw them in light gray)
	frontier.update({(6,2):True, (6,3):True, (6,4):True, (6,5):True, (6,6):True, (6,7):True})

	'''
	YOUR WORK HERE.
	
	I believe in you
		-Gunnar (the TA)-
	'''

	fil = open(filename,'a')

	planner = ANAPlanner(im,start,end)
	planner.ana_star()
	path.extend(planner.path)
	# print "Number of sub optimal solutions -- ",planner.sub_count
	expanded.update(planner.expanded)
	frontier.update(planner.frontier)
	ss = planner.stats
	print "Performance stats :\n",ss
	for k in ss.keys():
		ll = ss[k]
		fil.write(str(ll[0])+"|"+str(ll[1])+"|"+str(ll[2])+"|\n")
			# fil.write
	visualize_search(output_name) # see what your search has wrought (and maybe save your results)

def visualize_search(save_file="do_not_save.png"):
	"""
	:param save_file: (optional) filename to save image to (no filename given means no save file)
	"""
	im = Image.open(difficulty).convert("RGB")
	pixel_access = im.load()

	# draw start and end pixels
	pixel_access[start[0], start[1]] = NEON_GREEN
	pixel_access[end[0], end[1]] = NEON_GREEN


	npa = np.array(im)


	# draw frontier pixels
	for pixel in frontier.keys():
		pixel_access[pixel[0], pixel[1]] = LIGHT_GRAY

	# draw expanded pixels
	for pixel in expanded.keys():
		pixel_access[pixel[0], pixel[1]] = DARK_GRAY

	# draw path pixels
	for pixel in path:
		pixel_access[pixel[0], pixel[1]] = PURPLE
	# display and (maybe) save results
	im.show()
	if(save_file != "do_not_save.png"):
		im.save(save_file)

	im.close()


if __name__ == "__main__":
	# Throw Errors && Such
	# global difficulty, start, end
	time1 = time.time()
	assert sys.version_info[0] == 2                                 # require python 2 (instead of python 3)
	assert len(sys.argv) == 2, "Incorrect Number of arguments"      # require difficulty input

	# Parse input arguments
	function_name = str(sys.argv[0])
	difficulty = str(sys.argv[1])
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

	elif difficulty == "my.png":
		start = (0,20)
		end = (99,20)

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
		assert False, "Incorrect difficulty level provided"

	# Perform search on given image
	im = Image.open(difficulty)
	filename = difficulty[:-4]+"_stats_anastar.txt"
	output_name = difficulty[:-4]+"_anastar.png"
	Search(im.load(),output_name,filename)
	print time.time()-time1
