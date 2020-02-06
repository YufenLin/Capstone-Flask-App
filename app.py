from flask import Flask, send_from_directory, render_template, request, abort
from waitress import serve
from src.models.wine_predictor import predict_wine

from src.models.sommelier import check_user_exist, have_similar_user, recommend_wine, get_wine_id, recommend_from_top_rating, get_user_name, top_rating, query_wine
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
    # option = request.form['options']
    # print(data) 
    # print(data['user_id'])
    # test_value, errors = validate_input_user(data)
    # if not errors:
    if data['options'] == "option1":
        wine_id = int(data['wine_id'])
    if data['options'] == "option2":
        wine_title = data['wine_title']
        wine_id = get_wine_id(wine_title)
        
    top_n_similar_wine = recommend_wine(wine_id, n=5)
    return render_template("similar_wine.html", wine_id=wine_id, tables=[top_n_similar_wine.to_html(classes='my_df')], columns=top_n_similar_wine.columns.values)
    
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
            user_name = get_user_name(user_id)
            top_n_from_rating = recommend_from_top_rating(user_id)
            return render_template("user_exist_wo_similar.html", user_name=user_name, tables=[top_n_from_rating.to_html(classes='my_df')], columns=top_n_from_rating.columns.values)
        else:
            top_n_new_user = top_rating()
            return render_template("new_user.html",tables=[top_n_new_user.to_html(classes='my_df')], columns=top_n_new_user.columns.values)
    # else:
    #     return abort(400, errors)
@app.route("/get_wine_info", methods=["POST"])
def get_wine_info():
    """ Predict the class of wine based on the inputs. """
    data = request.form
    wine_cat = str(data['category'])
    wine_country = str(data['country'])
    # price_min = int(data['price_min'])
    price_max = int(data['price_max'])
    # user_id = int(data['user_id'])
    # print(wine_cat)
    result = query_wine(wine_cat, wine_country, price_max)

    return render_template("new_user.html",tables=[result.to_html(classes='my_df')], columns=result.columns.values)


if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=5000)
