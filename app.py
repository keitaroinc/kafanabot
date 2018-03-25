# encoding: utf-8

import json
import kafanabot
from flask import Flask, request, make_response, render_template
import requests
from foursquare import Foursquare
import os

pyBot = kafanabot.KafanaBot()
slack = pyBot.client

app = Flask(__name__)


@app.route("/install", methods=["GET"])
def pre_install():
    client_id = pyBot.oauth["client_id"]
    scope = pyBot.oauth["scope"]
    return render_template("install.html", client_id=client_id, scope=scope)


@app.route("/thanks", methods=["GET", "POST"])
def thanks():
    code_arg = request.args.get('code')
    return render_template("thanks.html")


@app.route("/kafana_auth", methods=["GET", "POST"])
def hears():
    slack_event = json.loads(request.data)

    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type":
                                                             "application/json"
                                                             })

    if pyBot.verification != slack_event.get("token"):
        message = "Invalid Slack verification token: %s \npyBot has: \
                   %s\n\n" % (slack_event["token"], pyBot.verification)

        make_response(message, 403, {"X-Slack-No-Retry": 1})

    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})


@app.route("/kafana", methods=["GET", "POST"])
def kafana_command():
    pyBot.post_message()
    client = foursquare.Foursquare(client_id=os.environ.get("FOURSQUARE_CLIENT_ID"), client_secret='FOURSQUARE_CLIENT_SECRET', redirect_uri='http://fondu.com/oauth/authorize')
    auth_uri = client.oauth.auth_url()
    print client
    return make_response("command", 200, {"content-type":
                                                        "application/json"
                                                        });


if __name__ == '__main__':
    app.run(debug=True)
