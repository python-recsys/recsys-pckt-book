import numpy as np

f = open('movies.data', 'w')

data_m = np.loadtxt('u.data',
            delimiter='\t', usecols=(0, 1, 2), dtype=int)

data_u = open('u.user')

dict_users = {}

for line in data_u:
    line = line.strip().split('::')
    dict_users[int(line[0])] = line[1]

for user, item, rating in data_m:
    f.write('%d\t%s\t%d\t%d\n' % (user, dict_users[int(user)], item, rating))

f.close()
#data_movies = {}
#for user_id, item_id, rating in data_m:
