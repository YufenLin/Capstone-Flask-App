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