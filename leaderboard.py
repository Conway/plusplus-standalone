from models import Thing


def generate_leaderboard():
    users = Thing.query.filter_by(user=True).order_by(Thing.points.desc()).limit(10)
    things = Thing.query.filter_by(user=False).order_by(Thing.points.desc()).limit(10)
    formatted_users = [f"<@{user.item.upper()}> ({user.points})" for user in users]
    formatted_things = [f"{thing.item} ({thing.points})" for thing in things]
    numbered_users = generate_numbered_list(formatted_users)
    numbered_things = generate_numbered_list(formatted_things)
    leaderboard_header = {"type": "section",
                          "text":
                              {"type": "mrkdwn",
                               "text": "Here's the current leaderboard:"
                               }
                          }
    body = {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*Users*\n" + numbered_users
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Things*\n" + numbered_things
                    }
                ]
        }
    leaderboard = [leaderboard_header, body]
    return json.dumps(leaderboard)


def generate_numbered_list(items):
    out = ""
    for i, item in enumerate(items, 1):
        out += f"{i}. {item}\n"
    if len(out) == 0:
        out = "Welp, nothing's here yet."
    return out
