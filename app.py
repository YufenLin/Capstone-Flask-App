from flask import Flask, send_from_directory, render_template, request, abort
from waitress import serve
from src.models.wine_predictor import predict_wine

from src.models.sommelier import check_user_exist
from src.utils import validate_input

app = Flask(__name__, static_url_path="/static")

@app.route("/")
def index():
    """Return the main page."""
    return send_from_directory("static", "index.html")

@app.route("/get_results", methods=["POST"])
def get_results():
    """ Predict the class of wine based on the inputs. """
    data = request.form
    print(data)
    
    print(data['user_id'])
    test_value, errors = validate_input(data)

    if not errors:
        # predicted_class = predict_wine(test_value)
        user_exist = check_user_exist(data['user_id'])
        if user_exist:
            return render_template("user_exist.html", user_id=user_exist)
        else:
            return render_template("new_user.html")
    else:
        return abort(400, errors)

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=5000)
