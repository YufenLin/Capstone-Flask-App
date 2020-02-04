import pickle
import pandas

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

def is_similar_user(in_user_id):
    wine_user = load_model()
    # There is error need to be fixed.
    wine_user_rating = wine_user.pivot_table(index = ["wine_id"], columns = ['taster_id'], values = "points")
    similarity_with_other_user = wine_user_rating.corrwith(wine_user_rating[in_user_id]) 
    similarity_with_other_user = similarity_with_other_user.sort_values(ascending=False)

    # similarity_user = similarity_with_other_user[similarity_with_other_user.index!=in_user_id]
    if similarity_with_other_user.values[1]>0.8:
        # print(similarity_with_other_user.index[1])
        similar_user = similarity_with_other_user.index[1]
        similar_user_top = get_user_top_n(similar_user, wine_user, n=5)
        
        return similar_user, similar_user_top
    else:
        print("No similar taste user.")
        return False
    # 7 - 19 
    # 8 >< 15
    # 14 - 16
def get_user_top_n(user_id, wine_user, n=5):
    return wine_user[wine_user['taster_id']==user_id].sort_values(by=['points'], ascending=False)[0:5][['wine_id','title']]