from flask import Flask
from slackeventsapi import SlackEventAdapter
from slackclient import SlackClient
from operations import process_match, generate_string
from leaderboard import generate_leaderboard
from models import db
import re
import config

# get Slack secret
operation_exp = re.compile(r"(<?@|#)(.+)(\+\+|\-\-|==)")

# flask init
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI

# init slack event adaptor
slack = SlackEventAdapter(config.SIGNING_SECRET, "/slack/events", app)

# init slack client
sc = SlackClient(config.SLACK_TOKEN)

# init SQLAlchemy
with app.app_context():
    db.init_app(app)
    db.create_all()


@slack.on("message")
def handle_message(event_data, req):
    # ignore retries
    if req.headers.get('X-Slack-Retry-Reason'):
        return "Status: OK"
    # ignore bot messages
    if 'subtype' in event_data['event'] and event_data['event']['subtype'] == 'bot_message':
        return "Status: OK"

    event = event_data['event']
    message = event.get('text').lower()
    user = event.get('user').lower()
    channel = event.get('channel')

    operation_match = operation_exp.match(message)
    if operation_match:
        thing, operation = process_match(operation_match, user)
        db.session.add(thing)
        db.session.commit()
        output = generate_string(thing, operation)
        sc.api_call(
            "chat.postMessage",
            channel=channel,
            text=output
        )
        print("Processed " + thing.item)
    elif "leaderboard" in message and config.BOT_KEYWORD in message:
        sc.api_call(
            "chat.postMessage",
            channel=channel,
            blocks=generate_leaderboard()
        )
        pass
    else:
        print(message)
        return
    return "OK", 200


if __name__ == '__main__':
    app.run(port=3000)
