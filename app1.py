from flask import Flask, request, jsonify
import pickle
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from math import floor
from flask_caching import Cache

app = Flask(__name__)

cache = Cache(app, config={'CACHE_TYPE': 'null'})
# Charger le data

clicks =pd.read_csv('/home/SaraDJEG/Projet9/clicks_sample.csv')
articles = pd.read_csv('/home/SaraDJEG/Projet9/articles_metadata.csv')


def cb_recommender(user_id, articles=articles, clicks=clicks, n=5):

    articles_read = clicks[clicks['user_id'] == user_id]['click_article_id'].tolist()

    if len(articles_read) == 0:
        return "L'utilisateur n'a lu aucun article"

    articles_read_embedding = articles.loc[articles_read]

    articles = articles.drop(articles_read)

    matrix = cosine_similarity(articles_read_embedding, articles)

    rec = []

    for i in range(n):
        coord_x = floor(np.argmax(matrix)/matrix.shape[1])
        coord_y = np.argmax(matrix)%matrix.shape[1]

        rec.append(int(articles.index[coord_y]))

        matrix[coord_x][coord_y] = 0

    return rec

@app.route('/')
def index():
    return 'Welcome P9 !'

@app.route('/recommendation', methods=['GET'])
def recommendation():

    user_id = request.args.get('user_id')

    recommendations = cb_recommender(int(user_id))
    # Retourner les recommandations en réponse
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)