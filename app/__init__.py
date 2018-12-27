import os
from slackclient import SlackClient
from flask import Flask, request
#from flask_sqlalchemy import SQLAlchemy

sc = SlackClient(os.environ('TOKEN'))
app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = environ['DATABASE_URL']
#db = SQLAlchemy(app)

from app import core_bot#, models

@app.route("/"+os.environ['TOKEN'], methods=['POST'])
def getMessage():
    request_json = request.get_json(silent=True, force=True)
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

app.run(host="0.0.0.0", port=int(os.getenv('PORT', 5000)))