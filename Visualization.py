import numpy as np
import matplotlib.pyplot as plt
from random import shuffle

# Read all the data
data = np.genfromtxt('data.txt',delimiter='\t',dtype='str')
movies = np.genfromtxt('movies.txt',delimiter='\t',dtype='str')
coords = np.genfromtxt('coords.csv',delimiter=",")

pathB = './Charts/Basic_'
path = './Charts/MF_'

# Make a dictionary with each movieID as a key and its coordinates as a value
movie_coords = {}
for i,(x,y) in enumerate(coords):
	movie_coords[i] = (x,y)

movieIDs = data[:,1]
movieRatings = data[:,2]

# Make a dictionary with each movieID as a key and the list of all its 
# ratings as a value
allMovies = {}
for i in range(len(movieIDs)):
	movieID = int(movieIDs[i])
	rating = int(movieRatings[i])

	if(movieID in allMovies.keys()):
		allMovies[movieID].append(rating)
	else:
		allMovies[movieID] = [rating]

# Dictionary matching a genre name to its column in the movies matrix
genreID = {'unknown': 2, 'action': 3, 'adventure': 4, 'animation': 5, \
	'childrens': 6, 'comedy': 7, 'crime': 8, 'documentary': 9, \
	'drama': 10, 'fantasy': 11, 'film-noir': 12, 'horror': 13, \
	'musical': 14, 'mystery': 15, 'romance': 16, 'sci-fi': 17, 'thriller': 18,\
	'war': 19, 'western': 20}

##############################################################################
# BASIC VISUALIZATIONS

# This function takes in data and builds a boxplot. It is used to 
# construct the visualization for the highestRated and mostPopular movies.
def buildBoxPlot(data_to_plot, xlabels, title, filename):

	fig = plt.figure(1, figsize=(9,6))
	ax = fig.add_subplot(111)

	bp = ax.boxplot(data_to_plot, showmeans=True)

	# Customize the x-axis labels
	ax.set_xticklabels(xlabels)
	for tick in ax.xaxis.get_major_ticks():
		tick.label.set_fontsize(10)
		tick.label.set_rotation('vertical')

	## Remove top axes and right axes ticks
	ax.get_xaxis().tick_bottom()
	ax.get_yaxis().tick_left()

	fig.suptitle(title)

	fig.savefig(filename, bbox_inches='tight')
	plt.close()

# This function makes a histogram of all the ratings that exist in our
# database.
def visualizeAllRatings():
	allRatings = []
	for key in allMovies:
		allRatings.extend(allMovies[key])

	plt.xlabel('Rating')
	plt.ylabel('Number of Movies')
	plt.title('Histogram of the Number of Ratings in the Dataset')
	plt.hist(allRatings, bins=5)
	plt.savefig(pathB+'AllRatings.png')
	plt.close()

# This function takes the n most popular movies (based on number of ratings)
# and sends it to the boxplot function.
def visualizeMostPopular(n):
	sortedDict = sorted(allMovies, key=lambda k: len(allMovies[k]), reverse=True)

	data_to_plot = []
	movieNames = []

	for i in range(n):
		index = sortedDict[i]
		data_to_plot.append(allMovies[index])
		movieNames.append(movies[(index-1),1])

	title = 'Most Popular Movies and their Ratings'
	filename = pathB+'popularMovies.png'
	buildBoxPlot(data_to_plot, movieNames, title, filename)

# This function takes the n highest rated (based on average rating and 
# number of ratings above a threshold) and sends the data to a boxplot 
# function to be visualized.
def visualizeHighestRated(n):
	threshold = 20

	averageRatings = {}
	for key in allMovies:
		if(len(allMovies[key]) >= threshold):
			averageRating = np.mean(allMovies[key])
			averageRatings[key] = averageRating

	sortedDict = sorted(averageRatings, key=lambda k: averageRatings[k], reverse=True)

	data_to_plot = []
	movieNames = []

	for i in range(n):
		index = sortedDict[i]
		data_to_plot.append(allMovies[index])
		movieNames.append(movies[(index-1),1])

	title = 'The Ratings of the Highest Rated Movies'
	filename = pathB+'highestRated.png'
	buildBoxPlot(data_to_plot, movieNames, title, filename)

# This function takes in some genre name and builds a histogram of all the
# movie ratings for movies in that genre.
def visualizeGenre(genre):
	genreNum = genreID[genre]
	# print(genreNum)
	allRatings = []
	for i in range(len(allMovies)):
		if(int(movies[i, genreNum])):
			allRatings.extend(allMovies[i+1])

	plt.xlabel('Rating')
	plt.ylabel('Number of Movies')
	title = 'Histogram of the Number of Ratings for a ' + genre.capitalize() + ' Movie'
	filename = genre+'Ratings.png'
	plt.title(title)
	plt.hist(allRatings, bins=5)
	plt.savefig(pathB+filename)
	plt.close()

########################
# Run all of our functions with the desired parameters.
visualizeAllRatings()
visualizeMostPopular(10)
visualizeHighestRated(10)
visualizeGenre('musical')
visualizeGenre('horror')
visualizeGenre('romance')
#########################

##############################################################################
# MATRIX FACTORIZATION VISUALIZATION

def scatterMostPopular(n):
	sortedDict = sorted(allMovies, key=lambda k: len(allMovies[k]), reverse=True)
	x_vals = []
	y_vals = []
	movieNames = []

	for i in range(n):
		index = sortedDict[i]
		x, y = movie_coords[index] 
		x_vals.append(x)
		y_vals.append(y)
		movieNames.append(movies[(index-1),1])
	plt.scatter(x_vals, y_vals)
	for name, x, y in zip(movieNames, x_vals, y_vals):
		plt.annotate(name,xy=(x, y),xytext=(-20, 20),textcoords='offset points',ha='right',va='bottom',arrowprops=dict(arrowstyle = '->',connectionstyle='arc3,rad=0'))
	plt.title('2-D Visualization of 10 Most Popular Movies')
	axes = plt.gca()
	axes.set_xlim([-2,2])
	axes.set_ylim([-2,2])
	plt.savefig(path+"MostPopular.png")
	plt.close()

def scatterRandom(n):
	sortedDict = sorted(allMovies, key=lambda k: len(allMovies[k]), reverse=True)
	shuffle(sortedDict)
	x_vals = []
	y_vals = []
	movieNames = []

	for i in range(n):
		index = sortedDict[i]
		x, y = movie_coords[index] 
		x_vals.append(x)
		y_vals.append(y)
		movieNames.append(movies[(index-1),1])
	plt.scatter(x_vals, y_vals)
	for name, x, y in zip(movieNames, x_vals, y_vals):
		plt.annotate(name,xy=(x, y),xytext=(-20, 20),textcoords='offset points',ha='right',va='bottom',arrowprops=dict(arrowstyle = '->',connectionstyle='arc3,rad=0'))
	plt.title('2-D Visualization of 10 Random Movies')
	axes = plt.gca()
	axes.set_xlim([-2,2])
	axes.set_ylim([-2,2])
	plt.savefig(path+"RandomMovies.png")
	plt.close()

def scatterHighestRated(n):
	threshold = 20

	averageRatings = {}
	for key in allMovies:
		if(len(allMovies[key]) >= threshold):
			averageRating = np.mean(allMovies[key])
			averageRatings[key] = averageRating

	x_vals = []
	y_vals = []

	sortedDict = sorted(averageRatings, key=lambda k: averageRatings[k], reverse=True)

	data_to_plot = []
	movieNames = []

	for i in range(n):
		index = sortedDict[i]
		x, y = movie_coords[index] 
		x_vals.append(x)
		y_vals.append(y)
		movieNames.append(movies[(index-1),1])
	plt.scatter(x_vals, y_vals)
	for name, x, y in zip(movieNames, x_vals, y_vals):
		plt.annotate(name,xy=(x, y),xytext=(-20, 20),textcoords='offset points',ha='right',va='bottom',arrowprops=dict(arrowstyle = '->',connectionstyle='arc3,rad=0'))
	plt.title('2-D Visualization of 10 Highest Rated Movies')
	axes = plt.gca()
	axes.set_xlim([-2,2])
	axes.set_ylim([-2,2])
	plt.savefig(path+"HighestRated.png")
	plt.close()

def scatterGenres(n,genre):
	genreNum = genreID[genre]
	genreMovies = []

	x_vals = []
	y_vals = []
	movieNames = []

	for i in range(len(allMovies)):
		if(int(movies[i, genreNum])):
			genreMovies.append(i)

	shuffle(genreMovies)
	for i in range(n):
		index = genreMovies[i]
		x, y = movie_coords[index] 
		x_vals.append(x)
		y_vals.append(y)
		movieNames.append(movies[(index),1])

	plt.scatter(x_vals, y_vals)
	for name, x, y in zip(movieNames, x_vals, y_vals):
		plt.annotate(name,xy=(x, y),xytext=(-20, 20),textcoords='offset points',ha='right',va='bottom',arrowprops=dict(arrowstyle = '->',connectionstyle='arc3,rad=0'))
	plt.title('2-D Visualization of 10 Random ' + genre.title() + ' Movies')
	axes = plt.gca()
	axes.set_xlim([-2,2])
	axes.set_ylim([-2,2])
	plt.savefig(path+genre.capitalize()+"Ratings.png")
	plt.close()


scatterMostPopular(10)
scatterRandom(10)
scatterHighestRated(10)
scatterGenres(10, 'musical')
scatterGenres(10, 'horror')
scatterGenres(10, 'romance')