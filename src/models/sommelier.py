import pickle
import pandas
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
    
    return top_n_df[['wine_id','title','country','price']]

#  def recommend_wine(wineid, n = 5, cosine_sim = tfidf_cos): 
#     with open("src/models/wine_train.pkl", 'rb') as f:
#         wine = pickle.load(f)
#     f.close()
#     indices = list(wine.wine_id)

#     # retrieve matching movie title index
#     if wineid not in indices:
#         print("Wine not in database.")
#         return
#     else:
#         print("Wine is in database.")
#         idx = wine[wine['wine_id'] == wineid].index[0]
#         print("Flavor:",wine[wine['wine_id'] == wineid]['flavor_words'])
#     # cosine similarity scores of movies in descending order
#     scores = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
    
#     # top n most similar movies indexes
#     # use 1:n because 0 is the same movie entered
#     top_n_idx = list(scores.iloc[0:n].index)
        
#     return wine['wine_id'].iloc[top_n_idx]