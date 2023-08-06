import os
from flask import Flask, request, jsonify
from .translator import Translator

app = Flask(__name__)
translator = Translator(os.environ.get("SOURCE_LANG"), os.environ.get("TARGET_LANG"), os.environ.get("MODEL_PATH"))

app.config["DEBUG"] = True # turn off in prod

@app.route('/', methods=["GET"])
def health_check():
    """Confirms service is running"""
    return "Machine translation service is up and running."

@app.route('/lang_routes', methods = ["GET"])
def get_lang_route():
    lang = request.args['lang']
    all_langs = translator.get_supported_langs()
    lang_routes = [l for l in all_langs if l[0] == lang]
    return jsonify({"routes":lang_routes})

@app.route('/supported_languages', methods=["GET"])
def get_supported_languages():
    langs = translator.get_supported_langs()
    return jsonify({"languages":langs})

@app.route('/translate', methods=["POST"])
def get_prediction():
    text = request.json['text']
    translation = translator.translate(text)
    return jsonify({"translation":translation})

app.run(host="0.0.0.0")