
import numpy as np
import matplotlib.pyplot as plt

V = np.genfromtxt('V.csv',delimiter=",")

A,S,B = np.linalg.svd(V, full_matrices = False)
B = np.transpose(B)
plot = B[:,:2]
#plot = np.dot(plot,np.transpose(V))
plot = plot / plot.max(axis=0)
print plot

movies = {}
for i,(x,y) in enumerate(plot):
	movies[i] = (x,y)

labels = []
#for i in range(10):


plt.scatter(plot[:,0],plot[:,1])
plt.show()