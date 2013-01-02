# -*- coding: utf-8 -*-

'''
Base Code for Chapter 01

'''
from os.path import dirname
import numpy as np
import matplotlib.pyplot as plt
import pickle


class Bunch(dict):
    """
    Container object for datasets: dictionary-like object
    that exposes its keys and attributes. """

    def __init__(self, **kwargs):
        dict.__init__(self, kwargs)
        self.__dict__ = self


def load_movie_lens():
    """ Load and return the MovieLens dataset with
        100,000 ratings (only the user ids, item ids, timestamps
        and ratings).

    """
    base_dir = dirname(__file__)

    dt = np.dtype({'names': ['user', 'sex', 'item', 'rating'],
        'formats': [np.int, 'S1', np.int, np.int]})

    #Read data
    data_movies = np.loadtxt(base_dir + 'movies.data',
                delimiter='\t', usecols=(0, 1, 2, 3), dtype=dt)

    #Read the titles
    data_titles = np.loadtxt(base_dir + 'u.item',
             delimiter='|', usecols=(0, 1), dtype=str)

    return Bunch(prefs=data_movies, item_ids=data_titles,
                     user_ids=np.unique(data_movies['user']))


def load_ratings_matrix(movie_data):
    saida = open('ratings.pk1', 'wb+')
    matrix = []
    for user in movie_data['user_ids']:
        matrix.append(
            [
            movie_data['prefs'][
            np.where((movie_data['prefs']['user'] == user) &
                    (movie_data['prefs']['item'] == int(item)))][0][3]
          if movie_data['prefs'][
            np.where((movie_data['prefs']['user'] == user) &
                    (movie_data['prefs']['item'] == int(item)))] else 0
                for item, title in movie_data['item_ids']])

    # I use pickle for searilize objects into files.
    pickle.dump(matrix, saida)
    return matrix


def plot_ratings_matrix(file_pickle='ratings.pk1'):
    file_h = open(file_pickle, 'rb')
    matrix = pickle.load(file_h)

    plt.pcolormesh(np.array(matrix), cmap=plt.get_cmap('hot'))
    plt.xlim(0, 1685)
    plt.ylim(0, 945)
    plt.title('Ratings Matrix for MovieLens 100k')
    plt.colorbar()
    plt.show()


#Read the movielens dataset.
movie_data = load_movie_lens()

print movie_data['item_ids'][:5]
print movie_data['prefs'][:5]
print movie_data['user_ids'][:5]


items = len(movie_data['item_ids'])
print items
ratings = len(movie_data['prefs'])
print ratings

users = len(movie_data['user_ids'])
print users

#Calculate the sparsity.
sparsity = 1.0 - (float(ratings) / (items * users))
print sparsity


#Let's visualize the ratings matrix
#OS:The first method can take some hours to process.

#load_ratings_matrix(movie_data)
#plot_ratings_matrix()


#Calcular os top-recommendations pelos mais populares com notas medias altas.
unique_ids = movie_data['item_ids']
ids = movie_data['prefs']['item']
ratings = movie_data['prefs']['rating']
top_items = []
for id, title in unique_ids:
    if ratings[ids == int(id)].size >= 100:
        top_items.append((title, ratings[ids == int(id)].size,
                        ratings[ids == int(id)].mean()))

top_items = sorted(top_items, key=lambda x: -x[2])
print 'title\t\traters\t\tscore'
for title, raters, score in top_items[:10]:
    print '%s\t\t%d\t\t%f' % (title, raters, score)


#Calcular os top-recommendations pelo sexo pelos mais assistidos.

unique_ids = movie_data['item_ids']
sex = movie_data['prefs']['sex']
male_rated_movies = movie_data['prefs'][sex == 'M']
female_rated_movies = movie_data['prefs'][sex == 'F']

male_ratings = male_rated_movies['rating']
female_ratings = female_rated_movies['rating']
movie_m_ids = male_rated_movies['item']
female_m_ids = female_rated_movies['item']

top_male_movies = []
top_female_movies = []

for id, title in unique_ids:
    if male_ratings[movie_m_ids == int(id)].size > 0:
        top_male_movies.append((title,
                    male_ratings[movie_m_ids == int(id)].size))

    if female_ratings[female_m_ids == int(id)].size > 0:
        top_female_movies.append((title,
                    female_ratings[female_m_ids == int(id)].size))

top_items = sorted(top_male_movies, key=lambda x: -x[1])
print 'title\t\tviews'
for title, views in top_items[:10]:
    print '%s\t\t%d' % (title, views)

top_items = sorted(top_female_movies, key=lambda x: -x[1])
print 'title\t\tviews'
for title, views in top_items[:10]:
    print '%s\t\t%d' % (title, views)


unique_ids = movie_data['item_ids']
ratings = movie_data['prefs']['rating']
ids = movie_data['prefs']['item']
sex = movie_data['prefs']['sex']

male_rated_movies = movie_data['prefs'][sex == 'M']
female_rated_movies = movie_data['prefs'][sex == 'F']

male_ratings = male_rated_movies['rating']
female_ratings = female_rated_movies['rating']

movie_m_ids = male_rated_movies['item']
female_m_ids = female_rated_movies['item']


#Calcular os top-recommendations pelas notas, homens gostaram e mulheres nao
#gostaram.
sorted_by_diff = []

for id, title in unique_ids:

    if ratings[ids == int(id)].size < 10:
        continue

    if male_ratings[movie_m_ids == int(id)].size > 0:
        male_movie_mean = male_ratings[movie_m_ids == int(id)].mean()
    else:
        male_movie_mean = 0.0

    if female_ratings[female_m_ids == int(id)].size > 0:
        female_movie_mean = female_ratings[female_m_ids == int(id)].mean()
    else:
        female_movie_mean = 0.0

    diff = male_movie_mean - female_movie_mean

    sorted_by_diff.append((title, male_movie_mean, female_movie_mean, diff))


top_items = sorted(sorted_by_diff, key=lambda x: -x[3])
print 'title\t\tmale_mean\t\tfemale_mean\t\tdiff'
for title, male_movie_mean, female_movie_mean, diff in top_items[:10]:
    print '%s\t\t%f\t\t%f\t\t%f' % (title, male_movie_mean, female_movie_mean,
                                        diff)

#Calcular os top-recommendations independente de sexo.
top_items = []

unique_ids = movie_data['item_ids']
ids = movie_data['prefs']['item']
ratings = movie_data['prefs']['rating']
top_items = []
for id, title in unique_ids:
    if ratings[ids == int(id)].size >= 100:
        top_items.append((title,
                        ratings[ids == int(id)].std()))

top_items = sorted(top_items, key=lambda x: -x[1])
print 'title\t\tstd'
for title, std in top_items[:10]:
    print '%s\t\t%f' % (title, std)
