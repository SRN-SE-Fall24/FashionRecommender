import functools
import os
from flask import (
    Blueprint,
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
import google.generativeai as genai
from . import contracts

from werkzeug.security import check_password_hash, generate_password_hash
from . import models
from datetime import datetime
from werkzeug.utils import secure_filename
from pathlib import Path

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    from projectsecrets.gemini_secret import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

recommendationsbp = Blueprint("recommendationsbp", __name__, url_prefix="/")

"""
payload = {
    "occasion" : <occasion_name>
    "culture" : <culture>
    "gender": <gender>
    "ageGroup": <ageGroup>
    "city":<city>
    "dateTimeInput":<dateTimeInput> format : YYYY-MM-DDTHH:MM:SS
}
"""


@recommendationsbp.route("/recommendations", methods=["POST"])
def get_recommendations():
    req_json_body = request.json
    culture = ""
    occasion = ""
    gender = ""
    ageGroup = ""
    city = ""
    userid = '1'

    if contracts.SessionParameters.USERID not in session:
        return (
            jsonify(
                {
                    "error": "user not logged in",
                    "error_code": contracts.ErrorCodes.USER_NOT_LOGGED_IN,
                }
            ),
            403,
        )

    userid = session[contracts.SessionParameters.USERID]

    user = models.User.query.filter_by(id=int(userid)).first()
    if contracts.RecommendationContractRequest.CULTURE_KEY in req_json_body:
        culture = req_json_body[contracts.RecommendationContractRequest.CULTURE_KEY]

    # take from the user table
    city = user.city

    dateInput = datetime.today().strftime("%Y-%m-%d")
    timeInput = datetime.now()

    if contracts.RecommendationContractRequest.GENDER_KEY in req_json_body:
        gender = req_json_body[contracts.RecommendationContractRequest.GENDER_KEY].lower(
        )
    else:
        # take from the user table
        gender = "Female"

    if contracts.RecommendationContractRequest.OCCASION_KEY in req_json_body:
        occasion = req_json_body[contracts.RecommendationContractRequest.OCCASION_KEY]

    # Age
    if contracts.RecommendationContractRequest.AGE_GROUP_KEY in req_json_body:
        ageGroup = req_json_body[contracts.RecommendationContractRequest.AGE_GROUP_KEY]

    from . import helper

    help = helper.RecommendationHelper()
    links = help.giveRecommendations(userid=userid, gender=gender, occasion=occasion, city=city,
                                     culture=culture, ageGroup=ageGroup, date=dateInput, time=timeInput)

    recommendations = dict()
    recommendations[contracts.RecommendationContractResponse.LINKS] = []
    for link in links:
        recommendations[contracts.RecommendationContractResponse.LINKS].append(
            link)

    response = model.generate_content(f'''
        You are a fashion recommender bot.
        Give 3 color palette suggestions with 5 colors each based on the following data:
        Occasion: {occasion},
        Culture: {culture},
        Gender: {gender},
        Age group: {ageGroup},
        City: {city}
        With each color specific clothing/accessory/item of that color.
        Return the output in following format where there are 5 colors in each palette and each palette is sorted by color prominence:
        [[[hexColor1,item1], [hexColor2,item2], [hexColor3,item3], [hexColor4,item4], [hexColor5,item5]], [...], [...]]
        The above response should be directly parsable by JSON.parse
        ''')
    recommendations['COLOR_PALETTES'] = response.text

    return jsonify(recommendations), 200


@recommendationsbp.route("/style_match", methods=["POST"])
def style_match():
    try:
        if "clothingImage" not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        clothing_image = request.files["clothingImage"]

        if clothing_image.filename == "":
            return jsonify({"error": "No file selected"}), 400

        temp_file_path = os.path.join(UPLOAD_FOLDER, clothing_image.filename)
        clothing_image.save(temp_file_path)

        myfile = genai.upload_file(Path(temp_file_path))

        prompt = '''Based on the uploaded image, can you suggest clothing items or outfit recommendations in JSON format?
            Include the following keys:
            - 'recommended_outfits': A list of outfit ideas with their names and descriptions in form [{'name':name, 'description':description}, ...].
            - 'style_tips': Any additional styling tips or details.'''

        result = model.generate_content([myfile, prompt])
        response = result.text

        os.remove(temp_file_path)

        return jsonify({"recommendations": response}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
