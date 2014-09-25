#! usr/bin/env python
__author__ = 'Katey Basye, Faye Ip'
__email__ = 'kbasye@ischool.berkeley.edu, faye@ischool.berkeley.edu'
__python_version = '2.7.2'
__can_anonymously_use_as_example = True 

class Person:

	def __init__(self, name, list_of_ratings):
		self.name = name
		self.list_of_ratings = list_of_ratings
		self.num_watched = self.count_num_watched()
		self.num_not_watched = len(self.list_of_ratings) - self.num_watched

	def count_num_watched(self):
		count = 0
		for rating in self.list_of_ratings:
			if rating != 0:
				count += 1
		return count

class Movie:

	def __init__(self, name):
		self.name = name
		self.num_times_watched = 0
		self.rating_sum = 0
		self.average_rating = 0


user_name = raw_input("What is your user name? ")

# Create list of movie objects
movies = []
movies_file = open('movies.txt', 'r')
movies_list = movies_file.readlines()
for name in movies_list:
	movie = Movie(name)	
	movies.append(movie)

# Create list of people objects
people = []
ratings_file = open('ratings.txt', 'r')
ratings_list = ratings_file.readlines()
for item in ratings_list:
	line = item.split(',')
	list_of_ratings = []
	for num in line[1:]:
		list_of_ratings.append(int(num))
	person = Person(line[0], list_of_ratings)
	people.append(person)
	if line[0] == user_name:
		searched_person = person
	else:
		list_of_ratings = [0 for i in range(len(movies_list))] 
		searched_person = Person(user_name, list_of_ratings)


# To calculate the average rating for each movie,

# First, find out how many times each movie was watched and the sum of the ratings.
# Store these values as attributes of each movie object for easy access later.
for movie in movies:
	for person in people:
		person.list_of_ratings[movies.index(movie)]
		movie.rating_sum += person.list_of_ratings[movies.index(movie)]
		# Exclude the zero scores by users who have not rated the movie
		if person.list_of_ratings[movies.index(movie)] != 0:
			movie.num_times_watched += 1

# Then, calculate average for each movie and store it as an attribute for the movie.
for movie in movies:
	if movie.num_times_watched != 0:
		movie.average_rating = float(movie.rating_sum) / float(movie.num_times_watched)

# For a given user, return the top rated movies that have not yet been watched by the user.

# Extract movie ratings from each movie, so they can be sorted. 
average_movie_ratings = []
for movie in movies:
	average_movie_ratings.append(movie.average_rating)
sorted_average_movie_ratings = sorted(average_movie_ratings)

# Reverse the sorted average movie rating list.
reversed_average_movie_ratings = []
for i in range(len(sorted_average_movie_ratings)-1,0,-1):
	reversed_average_movie_ratings.append(sorted_average_movie_ratings[i])

# For a given user, return the top rated movies that have not yet been watched by the user.

# Find the top rated movies in the movie object list.
# Create new list of these movie names, so that each rating is unique.
ranked_movie_names = []
for num in reversed_average_movie_ratings:
	for movie in movies:
		if num == movie.average_rating and movie.name not in ranked_movie_names:
			ranked_movie_names.append(movie.name)

print "Movies you have not watched:", searched_person.num_not_watched

print "Recommendations for User bart using Algorithm 1:"
print "Movie Name\n:Ave. Rating, No. of Ratings"
print "_" *10

counter = 0
# Match the top movie in the ranked_movie_names to the movie object in the movies list.
for movie_name in ranked_movie_names:
	for movie in movies:
		if movie.name == movie_name:
			top_movie = movies[movies.index(movie)]
	# Find the top five movies that the searched person has watched.
	if searched_person.list_of_ratings[movies.index(top_movie)] == 0:
		print top_movie.name +":", top_movie.average_rating, ", " , top_movie.num_times_watched
		counter += 1
		if counter == 5:
			break