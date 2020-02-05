from flask import Flask, send_from_directory, render_template, request, abort
from waitress import serve
from src.models.wine_predictor import predict_wine

from src.models.sommelier import check_user_exist, have_similar_user
from src.utils import validate_input_wine, validate_input_user

app = Flask(__name__, static_url_path="/static")

@app.route("/")
def index():
    """Return the main page."""
    return send_from_directory("static", "index.html")

@app.route("/get_wine", methods=["POST"])
def get_wine():
    """ Predict the class of wine based on the inputs. """
    data = request.form
    # print(data) 
    # print(data['user_id'])
    # test_value, errors = validate_input_user(data)
    # if not errors:
    wine_id = int(data['wine_id'])
    
    # tfidf_recommend_list = recommend_wine(wine_train, 89368, n=5, cosine_sim = test)

    # if True:
    #     # predicted_class = predict_wine(test_value)
    #     user_exist = check_user_exist(data['user_id'])
    #     if user_exist:
    #         user_id = int(data['user_id'])
            
    #         is_similar_user, similar_user, top_n = have_similar_user(user_id)
    #         if is_similar_user:
    #             return render_template("user_exist.html", user_id=user_id, similar_user=similar_user, tables=[top_n.to_html(classes='male')], columns=top_n.columns.values)   
    #         else:
    #             return render_template("user_exist_wo_similar.html", user_id=user_id, tables=[top_n.to_html(classes='male')], columns=top_n.columns.values)
    #     else:
    #         return render_template("new_user.html")

    # else:
    #     return abort(400, errors)


@app.route("/get_results", methods=["POST"])
def get_results():
    """ Predict the class of wine based on the inputs. """
    data = request.form
    # print(data) 
    # print(data['user_id'])
    # test_value, errors = validate_input_user(data)
    # if not errors:
    if True:
        # predicted_class = predict_wine(test_value)
        user_exist = check_user_exist(data['user_id'])
        if user_exist:
            user_id = int(data['user_id'])
            is_similar_user, similar_user, top_n = have_similar_user(user_id)
            if is_similar_user:
                return render_template("user_exist.html", user_id=user_id, similar_user=similar_user, tables=[top_n.to_html(classes='male')], columns=top_n.columns.values)   
            else:
                return render_template("user_exist_wo_similar.html", user_id=user_id, tables=[top_n.to_html(classes='male')], columns=top_n.columns.values)
        else:
            return render_template("new_user.html")
    # else:
    #     return abort(400, errors)

    

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=5000)
