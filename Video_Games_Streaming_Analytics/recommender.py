'''
Recommender API
'''
import pandas as pd
import numpy as np
from collections import defaultdict
import pickle
import surprise
from surprise import Dataset, accuracy, Reader, NMF, NormalPredictor, BaselineOnly, CoClustering, SlopeOne, SVD, KNNBaseline
from surprise.model_selection import GridSearchCV, cross_validate, train_test_split


#First, we make sure our records match their inputs and augment as needed:
def load_models():
    with open( "Data/genres.pkl", "rb" ) as f:
        genres = pickle.load(f)

    with open( "Data/SlopeOne_genre_model.pkl", "rb" ) as f:
        algo_genre_user = pickle.load(f)

    with open( "Data/games.pkl", "rb" ) as f:
        games = pickle.load(f)

    with open( "Data/BaselineOnly_game_model.pkl", "rb" ) as f:
        algo_game_user = pickle.load(f)
    return genres, algo_genre_user, games, algo_game_user

def display_current_genres(streamer_name,genres):
    user_genres = list(genres[genres['user_name']==streamer_name]['game_genres'])
    return user_genres

def display_current_games(streamer_name, games):
    user_games = list(games[games['user_name']==streamer_name]['game_name'])
    return user_games


#Predicting Similar Genres/Games Based on User experience (user-based similarity) #
def get_top_n(predictions, n=10):
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n

def get_game_pic_urls(game_list):
    pic_url_list=list()
    with open( "Data/pic_url_dict.pkl", "rb" ) as f:
        games = pickle.load(f)
    for item in game_list:
        pic_url_list.append(games[item])

    return pic_url_list


def make_prediction(streamer_name,streamer_genres,streamer_games):
    '''
    Given the name of a streamer, list of genres they enter, and a list of games they say
    they play, generate predictions based on similar genres and similar games to both
    what they enter into our website and what our database has recorded for them.
    '''
    genres, algo_genre_user, games, algo_game_user = load_models()
    print(len(games['game_name'].unique()))

    # Look at genres of games that the streamer is currently playing using our database
    recorder_genre_list = display_current_genres(streamer_name, genres)
    #recorder_genre_list = display_current_genres(streamer_name, genres)
    # Combine above with the genres the streamer has entered into our website
    full_genres = set(recorder_genre_list + streamer_genres)
    full_genres = list(full_genres)

    # Repeat above for games
    recorder_game_list = display_current_games(streamer_name, games)
    # recorder_game_list = display_current_games(streamer_name, games)
    full_games = set(recorder_game_list + streamer_games)
    full_games = list(full_games)

    genre_iids = genres['game_genres'].unique()
    genre_iids_to_predict = np.setdiff1d(genre_iids, full_genres, assume_unique=True)

    # We are filling 'real' user rating of item to 4, but this does NOT have any effect on prediction

    genre_testset_personal = [[streamer_name, iid, 4.] for iid in genre_iids_to_predict]

    genre_personal_predictions = algo_genre_user.test(genre_testset_personal)
    genre_top_n = get_top_n(genre_personal_predictions)

    for uid, genre_user_ratings in genre_top_n.items():
        genre_user_based_list = [iid for (iid, _) in genre_user_ratings]

    game_iids = games['game_name'].unique()
    game_iids_to_predict = np.setdiff1d(game_iids, full_games, assume_unique=True)

    game_testset_personal = [[streamer_name, iid, 4.] for iid in game_iids_to_predict]

    game_personal_predictions = algo_game_user.test(game_testset_personal)
    game_top_n = get_top_n(game_personal_predictions)

    for uid, game_user_ratings in game_top_n.items():
        game_user_based_list = [iid for (iid, _) in game_user_ratings]

   
    genre_recommendations = set(genre_user_based_list)
    game_recommendations = set(game_user_based_list)

    return_dict = dict()
    input_dict = dict()
    input_dict['streamer_name'] = streamer_name
    input_dict['streamer_genres'] = streamer_genres
    input_dict['streamer_games'] = streamer_games
    input_values = input_dict
    return_dict['genre_recommendations'] = genre_recommendations
    return_dict['game_recommendations'] = game_recommendations

    game_pic_urls = get_game_pic_urls(game_recommendations)
    game_pic_urls = [x.replace('-{width}x{height}','') for x in game_pic_urls]
    return return_dict, game_pic_urls[:10]


# For troubleshooting, pass some default parameters
if __name__ == '__main__':
    pass

    # streamer_name = 'Ninja'
    # streamer_genres = 'Action'
    # streamer_games = 'Fortnite'


    # recommendations,pic_urls = make_prediction(streamer_name,streamer_genres,streamer_games)
    # print('Input Values: ',input_values['streamer_name'],
    #                         input_values['streamer_genres'],
    #                          input_values['streamer_games']  )

    # print('Genres: ', recommendations['genre_recommendations'])
    # print('Games: ', recommendations['game_recommendations'])
