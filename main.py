import random
import flask
from flask import Flask
app = Flask(__name__)

@app.route('/', methods=['POST'])
def hello_world():
  user_id = flask.request.form['userId']
  if 'movieId' in flask.request.form:
    # Add movie
    movie_id = flask.request.form['movieId']
  else:
    # Request movie
    movie_id = '---'
  return 'OK' + user_id + movie_id

@app.route('/request_movies', methods=['POST'])
def request_movies():
  requested_user = flask.request.form['userId']
  user_to_movies = dict()
  with open('./data/viewing_log.txt') as input_stream:
    for line in input_stream:
      user_id = line.split(',')[0]
      movie_id = line[:-1].split(',')[1]
      if user_id in user_to_movies:
        user_to_movies[user_id].append(movie_id)
      else:
        user_to_movies[user_id] = [movie_id]
  if requested_user in user_to_movies:
    last_users_movie = user_to_movies[requested_user][-1]
    # print(last_users_movie, type(last_users_movie))
    with open('./data/similarity_output.txt') as input_stream:
      list_of_movies = [0] * 5
      for line in input_stream:
        movie_id = int(line.split(',')[0])
        if movie_id == int(last_users_movie):
          recommended_movie = int(line[:-1].split(',')[1])
          list_of_movies = [recommended_movie, 0, 0, 0, 0]
          break
  else:
    # list_of_movies = random.sample(range(17000), 5)
    list_of_movies = [0] * 5
  return '[' + ','.join(map(str, list_of_movies)) + ']'

@app.route('/post_movie', methods=['POST'])
def post_movie():
  user_id = flask.request.form['userId']
  movie_id = flask.request.form['movieId']
  with open('./data/viewing_log.txt', 'a') as output_stream:
    output_stream.write(str(user_id) + ',' + str(movie_id) + '\n')
  return 'OK'

if __name__ == '__main__':
  app.run(debug=True)

