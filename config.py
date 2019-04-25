import os

VERSION = 0.1
NAME = "PlusPlusV2"
BOT_KEYWORD = "plusplus".lower()
SIGNING_SECRET = os.environ.get('SLACK_SIGNING_SECRET')
SLACK_TOKEN = os.environ.get('SLACK_BOT_USER_OAUTH_ACCESS_TOKEN')
