import matplotlib.pyplot as plt 
import numpy as np 


fn = raw_input("enter file name:: ")
f = open(fn+'_stats_anastar.txt','r')
f = f.readlines()
e = []
g = []
t = 0
for i in f:
	line = i.split('|')
	t += float(line[2])*100
	e.append([t,round(float(line[1]))])
	g.append([t,round(float(line[0]))])
print e
e = np.array(e)
g = np.array(g)
plt.figure(1)
plt.subplot(121)
plt.xlabel('time (seconds/100)')
plt.ylabel('Sub-optimality')
plt.grid(True)
# if(e[0,1]>100):
# plt.plot(e[1:,0],e[1:,1])
# else:
plt.step(e[:,0],e[:,1],lw=2)
plt.subplot(122)
plt.xlabel('time (seconds/100)')
plt.ylabel('Cost')
plt.step(g[:,0],g[:,1],lw=2)
plt.grid(True)
# plt.savefig(fn+"_plot.png",bbox_inches='tight')

plt.show()