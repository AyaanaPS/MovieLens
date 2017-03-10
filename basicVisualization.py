import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt('data.txt',delimiter='\t',dtype='str')
movies = np.genfromtxt('movies.txt',delimiter='\t',dtype='str')

allMovies = {}

movieIDs = data[:,1]
movieRatings = data[:,2]

for i in range(len(movieIDs)):
	movieID = int(movieIDs[i])
	rating = int(movieRatings[i])

	if(movieID in allMovies.keys()):
		allMovies[movieID].append(rating)
	else:
		allMovies[movieID] = [rating]

genreID = {'unknown': 2, 'action': 3, 'adventure': 4, 'animation': 5, \
	'childrens': 6, 'comedy': 7, 'crime': 8, 'documentary': 9, \
	'drama': 10, 'fantasy': 11, 'film-noir': 12, 'horror': 13, \
	'musical': 14, 'mystery': 15, 'romance': 16, 'sci-fi': 17, 'thriller': 18,\
	'war': 19, 'western': 20}

# I got help with the creating a boxplot from this site: 
# http://blog.bharatbhole.com/creating-boxplots-with-matplotlib/
def buildBoxPlot(data_to_plot, xlabels, title, filename):

	fig = plt.figure(1, figsize=(9,6))
	ax = fig.add_subplot(111)

	## add patch_artist=True option to ax.boxplot() 
	## to get fill color
	bp = ax.boxplot(data_to_plot, patch_artist=True)

	## change outline color, fill color and linewidth of the boxes
	for box in bp['boxes']:
	    # change outline color
	    box.set( color='#7570b3', linewidth=2)
	    # change fill color
	    box.set( facecolor = '#1b9e77' )

	## change color and linewidth of the whiskers
	for whisker in bp['whiskers']:
	    whisker.set(color='#7570b3', linewidth=2)

	## change color and linewidth of the caps
	for cap in bp['caps']:
	    cap.set(color='#7570b3', linewidth=2)

	## change color and linewidth of the medians
	for median in bp['medians']:
	    median.set(color='#b2df8a', linewidth=2)

	## change the style of fliers and their fill
	for flier in bp['fliers']:
	    flier.set(marker='o', color='#e7298a', alpha=0.5)

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

def visualizeAllRatings():
	allRatings = []
	for key in allMovies:
		allRatings.extend(allMovies[key])

	plt.xlabel('Rating')
	plt.ylabel('Number of Movies')
	plt.title('Histogram of the Number of Ratings in the Dataset')
	plt.hist(allRatings, bins=5)
	plt.savefig('AllRatings.png')

def visualizeMostPopular(n):
	sortedDict = sorted(allMovies, key=lambda k: len(allMovies[k]), reverse=True)

	data_to_plot = []
	movieNames = []

	for i in range(n):
		index = sortedDict[i]
		data_to_plot.append(allMovies[index])
		movieNames.append(movies[(index-1),1])

	title = 'Most Popular Movies and their Ratings'
	filename = 'popularMovies.png'
	buildBoxPlot(data_to_plot, movieNames, title, filename)

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
	filename = 'highestRatings.png'
	buildBoxPlot(data_to_plot, movieNames, title, filename)

# def visualizeGenre(genre):
# 	genreNum = genreID[genre]
# 	print(genreNum)
# 	allRatings = []
# 	for i in range(len(allMovies)):
# 		if(int(movies[i, genreNum])):
# 			print(movies[i, 1])
# 			allRatings.extend(allMovies[i+1])

	


# visualizeAllRatings()
# visualizeMostPopular(10)
# visualizeHighestRated(10)
# visualizeGenre('musical')

