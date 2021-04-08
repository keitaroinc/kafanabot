"""
Copyright (c) 2018 Keitaro AB

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

# encoding: utf-8

import os
#import message
import requests

from slackclient import SlackClient

authed_teams = {}


class KafanaBot(object):
    def __init__(self):
        super(KafanaBot, self).__init__()
        self.name = "kafanabot"
        self.emoji = ":robot_face:"

        self.oauth = {"client_id": os.environ.get("SLACK_CLIENT_ID"),
                      "client_secret": os.environ.get("SLACK_CLIENT_SECRET"),
                      "scope": "bot"}
        self.verification = os.environ.get("SLACK_VERIFICATION_TOKEN")

        self.client = SlackClient("")

        #self.messages = {}

    def auth(self, code):
        auth_response = self.client.api_call(
                                "oauth.access",
                                client_id=self.oauth["client_id"],
                                client_secret=self.oauth["client_secret"],
                                code=code
                                )

        team_id = auth_response["team_id"]
        authed_teams[team_id] = {"bot_token":
                                 auth_response["bot"]["bot_access_token"]}

        self.client = SlackClient(authed_teams[team_id]["bot_token"])


    def post_message(self):
        pass

