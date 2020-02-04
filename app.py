from flask import Flask, send_from_directory, render_template, request, abort
from waitress import serve
from src.models.wine_predictor import predict_wine

from src.models.sommelier import check_user_exist, is_similar_user
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
    # test_value, errors = validate_input_wine(data)

    # if not errors:
    if True:
        # predicted_class = predict_wine(test_value)
        user_exist = check_user_exist(data['user_id'])
        
        if user_exist:
            user_id = int(data['user_id'])
            similar_user = is_similar_user(user_id)
            if similar_user:
                return render_template("user_exist.html", user_id=user_id, similar_user=similar_user)
            else:
                return render_template("user_exist_wo_similar.html", user_id=user_id)
        else:
            return render_template("new_user.html")
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
            similar_user, similar_user_top = is_similar_user(user_id)

            if similar_user:
                return render_template("user_exist.html", user_id=user_id, similar_user=similar_user, tables=[similar_user_top.to_html(classes='data')], titles=similar_user_top.columns.values)
            else:
                return render_template("user_exist_wo_similar.html", user_id=user_id)
        else:
            return render_template("new_user.html")
    # else:
    #     return abort(400, errors)

    

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=5000)
