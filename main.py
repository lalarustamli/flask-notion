from flask import Flask, render_template

import utils
import config

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html",
                           title=utils.get_page_title(config.HOME_BLOCK),
                           raw_html=utils.parse_content(config.HOME_BLOCK))

@app.route('/<string:page_uuid>')
def sample_page(page_uuid):
    return render_template("index.html",
                           title=utils.get_page_title(page_uuid),
                           raw_html=utils.parse_content(page_uuid))
