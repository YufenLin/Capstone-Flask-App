import pickle
import pandas as pd
import numpy as np
from surprise import Reader, Dataset, SVD
from surprise.model_selection import train_test_split

def check_user_exist(in_user_id):
    wine_user = load_model()
    # return type(wine_user)
    return int(in_user_id) in wine_user['taster_id'].value_counts().index
    # if in_user_id == 0:
    #     return False
    # else:
    #     # return int(in_user_id)
    #     return int(in_user_id) in wine_user['taster_id'].value_counts().index

def load_model():
    """ Load the model from the .pickle file """
    with open("src/models/wine_user.pkl", 'rb') as f:
        data = pickle.load(f)
    f.close()
    # model_file = open("src/models/wine_user.pkl", "rb")
    # loaded_model = pickle.load(model_file)
    # model_file.close()
    return data

def have_similar_user(in_user_id):
    wine_user = load_model()
    # There is error need to be fixed.
    wine_user_rating = wine_user.pivot_table(index = ["wine_id"], columns = ['taster_id'], values = "points")
    similarity_with_other_user = wine_user_rating.corrwith(wine_user_rating[in_user_id]) 
    similarity_with_other_user = similarity_with_other_user.sort_values(ascending=False)

    # similarity_user = similarity_with_other_user[similarity_with_other_user.index!=in_user_id]
    if similarity_with_other_user.values[1]>0.8:
        is_similar_user = True
        # print(similarity_with_other_user.index[1])
        similar_user = similarity_with_other_user.index[1]
        similar_user_top = get_user_top_n(similar_user, wine_user, n=5)
        
        return is_similar_user, similar_user, similar_user_top
    else:
        is_similar_user = False
        similar_user = "None"
        # print("No similar taste user.")
        top_n = get_collab_top_n(in_user_id, wine_user, n=5)
        # print(top_n)
        return is_similar_user, similar_user, top_n
    # 7 - 19 
    # 8 >< 15
    # 14 - 16

def get_user_top_n(user_id, wine_user, n=5):
    return wine_user[wine_user['taster_id']==user_id].sort_values(by=['points'], ascending=False)[0:5][['wine_id','title','country','price']]

def get_collab_top_n(user_id, wine_user, n=5):
    reader = Reader(rating_scale=(80, 100))
    wine = Dataset.load_from_df(wine_user[['taster_id', 'wine_id', 'points']], reader)
    # test set is made of 25% of the ratings.
    trainset, testset = train_test_split(wine, test_size=0.25)
    algo = SVD()
    algo.fit(trainset)
    predictions = algo.test(testset)
    top_n = []
    for uid, iid, true_r, est, _ in predictions:
        if uid == user_id:
            top_n.append((iid,est))
    user_ratings = top_n        
    user_ratings.sort(key=lambda x: x[1], reverse=True)
    top_n= user_ratings[:n]
    top_n_list = [i[0] for i in top_n]
    top_n_df = get_wine_data(top_n_list, wine_user)
    
    return top_n_df

def get_wine_data(wine_id_list, wine_user):
    top_n_df = wine_user[wine_user['wine_id'].isin(wine_id_list)]
    top_n_df = top_n_df.sort_values("wine_id") 
    top_n_df.drop_duplicates(subset ="wine_id", keep = 'first', inplace = True) 
    
    return top_n_df[['wine_id','title','country','price','category','points','flavor_words_str', 'description']]
    # return top_n_df[['title','country','price', 'description']]

def get_from_cos(wineid, wine, n, cosine_sim):
    indices = list(wine.wine_id)
    if wineid not in indices:
        return []
    else:
        idx = wine[wine['wine_id'] == wineid].index[0]
    scores = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
    
    # top n most similar wine indexes
    # use 1:n because 0 is the same wine entered
    top_n_idx = list(scores.iloc[1:n+1].index)
    
    return top_n_idx

def recommend_wine(wineid, n = 5):
    with open("src/models/wine_train.pkl", 'rb') as f:
        wine = pickle.load(f)
    f.close()
    cosine_sim = np.load("src/models/outfile.npy")

    top_n_idx = get_from_cos(wineid, wine, n, cosine_sim)
    # query_wine = get_wine_data(list(wine.iloc[wineid]['wine_id']) , wine)
    top_n_wine = get_wine_data(list(wine.iloc[top_n_idx]['wine_id']) , wine)
    return top_n_wine

def get_wine_id(title):
     wine_user = load_model()
     df = wine_user[wine_user['title']==title]
     if df.shape[0]==0:
         return df.shape[0], []
     else:
         return df.shape[0], df['wine_id'].values[0]

def recommend_from_top_rating(user_id):
    with open("src/models/wine_train.pkl", 'rb') as f:
        wine = pickle.load(f)
    f.close()
    cosine_sim = np.load("src/models/outfile.npy")

    user_top_rating = wine[wine['taster_id']==user_id].sort_values(by='points', ascending=False).head(10)
    user_top_rating = user_top_rating.loc[:, 'wine_id'].values
    recommend_from_rating = []
    n = 5
    for wine_id in user_top_rating:
        recommend_from_rating += (get_from_cos(wine_id, wine, n, cosine_sim))
    keep_wine_id = []
    for wine_id in recommend_from_rating:
        if (wine[wine['wine_id']==wine_id]['taster_id']==user_id).any():
            pass
        else:
            keep_wine_id.append(wine_id)
        if len(keep_wine_id)>10:
            break

    keep_wine_id_df = get_wine_data(keep_wine_id, wine)

    return keep_wine_id_df

def get_user_name(user_id):
    with open("src/models/user.pkl", 'rb') as f:
        user = pickle.load(f)
    f.close()
    return user[user['taster_id']==user_id]['taster_name'].values[0]

def top_rating():
    with open("src/models/wine_user.pkl", 'rb') as f:
        wine_user = pickle.load(f)
    f.close()

    wine = wine_user[['wine_id','title','points']]
    points_mean = wine.groupby('wine_id')['points'].mean()
    wine.drop(['points'], axis=1, inplace=True)
    wine = wine.drop_duplicates('wine_id')
    wine = wine.sort_values(by='wine_id')
    wine['mean'] = points_mean.values
    # wine = wine.reset_index(drop=True)

    top_rating_id = wine.sort_values(by='mean',ascending=False).head()['wine_id'].values
    top_rating_df = get_wine_data(top_rating_id, wine_user)

    return top_rating_df

def top_rating_find_wine(wine_user):
    wine = wine_user[['wine_id','title','points']]
    points_mean = wine.groupby('wine_id')['points'].mean()
    wine.drop(['points'], axis=1, inplace=True)
    wine = wine.drop_duplicates('wine_id')
    wine = wine.sort_values(by='wine_id')
    wine['mean'] = points_mean.values
    # wine = wine.reset_index(drop=True)

    top_rating_id = wine.sort_values(by='mean',ascending=False).head()['wine_id'].values
    top_rating_df = get_wine_data(top_rating_id, wine_user)

    return top_rating_df

def query_wine(cat, country, price_max):
    with open("src/models/wine_user.pkl", 'rb') as f:
        wine_user = pickle.load(f)
    f.close()

    result = wine_user[wine_user['category']==cat]
    country_list = ['US', 'France', 'Italy', 'Spain', 'Portugal', 'Chile']
    
    if country in country_list:
        result = result[result['country']==country]
    else:
        result = result[~result['country'].isin(country_list)]
    result = result[result['price']<=price_max]


    resutlt = top_rating_find_wine(result)
    result_id = result['wine_id'].head().values
    result_df = get_wine_data(result_id, wine_user)

    return result_df

def get_similar_title(wine_title):
    with open("src/models/wine_train.pkl", 'rb') as f:
        wine = pickle.load(f)
    f.close()
    result_id = wine[wine['title'].str.contains(wine_title)]['wine_id'].values
    result_df = get_wine_data(result_id, wine)

    return result_df
