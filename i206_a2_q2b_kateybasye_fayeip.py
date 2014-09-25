#! usr/bin/env python
#! usr/bin/env python
__author__ = 'Katey Basye, Faye Ip'
__email__ = 'kbasye@ischool.berkeley.edu, faye@ischool.berkeley.edu'
__python_version = '2.7.2'
__can_anonymously_use_as_example = True

class Person:

    def __init__(self, name, list_of_ratings):
        self.name = name
        self.list_of_ratings = list_of_ratings
        self.watched_list = self.find_watched_list()
        self.num_watched = 0
        for i in self.watched_list:
            if i == True:
                self.num_watched += 1

    def find_watched_list(self):
        ##Returns a boolean list of whether a movie is watched or not
        watched_list = []
        for rating in self.list_of_ratings:
            if rating > 0:
                watched_list.append(True)
            else:
                watched_list.append(False)
        return watched_list


class Movie:

    def __init__(self, name):
        self.name = name
        self.num_times_rated = 0
        self.ratings_sum = 0
        self.ave_rating = 0
        self.soulmate_rating = 0
        

class RatingSystem:

    def __init__(self, people, movies):
        self.people = people
        self.movies = movies
        self.global_stats = self.compute_global_stats() 

    def compute_global_stats(self):
        #Computes avg ratings for each movie, num of times rated, ratings sum
        num_times_rated = [0 for i in range(len(self.movies))]
        ratings_sum = [0 for i in range(len(self.movies))]
        ave_ratings = [0 for i in range(len(self.movies))]

        for i in range(len(self.people)):
            for j in range(len(self.people[i].list_of_ratings)):
                ratings_sum[j] += self.people[i].list_of_ratings[j]
                if self.people[i].watched_list[j]:
                    num_times_rated[j] += 1

        for i in range(len(ave_ratings)):
            if num_times_rated[i] > 0:
                ave_ratings[i] = float(ratings_sum[i]) / float(num_times_rated[i])

        for i in range(len(self.movies)):
            self.movies[i].num_times_rated = num_times_rated[i]
            self.movies[i].ratings_sum = ratings_sum[i]
            self.movies[i].ave_rating = ave_ratings[i]

        return [num_times_rated, ratings_sum, ave_ratings]

    def movies_bubblesort(self, movies_list, soulmate_rank = True):
        #Returns a ranked list of movies by ave ratings, highest to lowest
        length = len(movies_list)

        if soulmate_rank:
            #Ranks based on soulmate's rating of movies
            for i in range(length, 1, -1):
                for j in range(0, i-1):
                    if movies_list[j].soulmate_rating < movies_list[j+1].soulmate_rating:
                        temp = movies_list[j]
                        movies_list[j] = movies_list[j+1]
                        movies_list[j+1] = temp
        else:
            #Ranks based on global average ratings of movies
            for i in range(length, 1, -1):
                for j in range(0, i-1):
                    if movies_list[j].ave_rating < movies_list[j+1].ave_rating:
                        temp = movies_list[j]
                        movies_list[j] = movies_list[j+1]
                        movies_list[j+1] = temp

        return movies_list 
        

    def match(self, person1, person2):
        ##Computes the 'match' score between the given user and another user
        score = 0
        for i in range(0, len(person1.list_of_ratings)):
            if person1.watched_list[i] == person2.watched_list[i]:
                rating1, rating2 = person1.list_of_ratings[i], person2.list_of_ratings[i]
                score += self.calculate_match_score(rating1, rating2)
        return score

    def calculate_match_score(self, rating1, rating2):
        return (rating1 + rating2) - (abs(rating1 - rating2))/(2.0) 

    def best_match(self, given_user):
        ##Runs 'match' method on all users and rewrites best if score is higher than previous best
        best = [given_user, 0]
        for other in self.people:
            if other != given_user:
                score = self.match(given_user, other)
                if score > best[1]:
                    best[0], best[1] = other, score
        return best


if __name__ == "__main__":

    #Read input from files
    try:
        ratings_file = open("ratings.txt", 'r')
        movies_file = open("movies.txt", 'r') 
    except IOError:
        print("Can't open input file")
        os.exit(1)

    rating_lines_list = ratings_file.readlines()
    movies_list = movies_file.readlines()
    ratings_file.close()
    movies_file.close()

    given_user = None 
    user_input = raw_input("What is your user name? ")

    #Build list of people objects
    people = []
    for line in rating_lines_list:
        cleaned_line = line.strip().split(',')
        list_of_ratings = []
        for num in cleaned_line[1:]:
            list_of_ratings.append(int(num))
        person = Person(cleaned_line[0], list_of_ratings)
        people.append(person)
        if cleaned_line[0] == user_input:
            given_user = person


    #Build list of movie objects
    movies = []
    for line in movies_list:
        movies.append(Movie(line.strip()))
    

    #Instantiate a rating system and find soulmate
    rs = RatingSystem(people, movies)
    if given_user != None:
        soulmate = rs.best_match(given_user)

    
    #Find 5 recommendations based on soulmate's ranked movies
    counter = 0
    recommended_list = []
    if given_user != None:
        #Calculate soulmate's ranked list of movies
        for i in range(len(soulmate[0].list_of_ratings)):
            rs.movies[i].soulmate_rating = soulmate[0].list_of_ratings[i]
            soulmate_movies_ranked = rs.movies_bubblesort(rs.movies, True)
        #Build recommended list
        for movie in soulmate_movies_ranked:
            if counter < 5 and given_user.watched_list[rs.movies.index(movie)] == False:
                recommended_list.append(movie)
                counter += 1
    else:
        global_ranked_movies = rs.movies_bubblesort(rs.movies, False)
        for movie in global_ranked_movies:
            if counter < 5:
                recommended_list.append(movie)
                counter += 1        
        
    
    #Print output for user
    if given_user != None:
        print "Your movie soul-mate is ", soulmate[0].name
        print "Your soul-mate score is ", soulmate[1]
        print "The top movie recommendations for %s are: " % user_input
        for movie in recommended_list:
            print movie.name
            print "  Rating by soul-mate: ", movie.soulmate_rating
            print "  Average rating: ", movie.ave_rating
            print "  Number of ratings: ", movie.num_times_rated
    else:
        print "The top movie recommendations for %s are: " % user_input
        for movie in recommended_list: 
            print movie.name
            print "  Average rating: ", movie.ave_rating
            print "  Number of ratings: ", movie.num_times_rated






    
