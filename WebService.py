import datetime
import json
import os

from flask import Flask, request

from TodoistSorter import Sorter

app = Flask(__name__)


@app.route("/todoist", methods=['POST'])
def webhook():
    project = os.getenv("PROJECT", None)
    api_token = os.getenv("APITOKEN", None)

    if None in (project, api_token):
        print("Environment variables cannot be None - exiting.")
        exit(1)

    bytesData = request.data.decode('ASCII')
    body = json.loads(bytesData)

    # USED FOR VERBOSE LOGGING
    print(json.dumps(body, indent=4, sort_keys=True))
    print("----------------------------")

    event_name = body['event_name']
    event_data = body['event_data']
    item_id = event_data['id']
    project_id = event_data['project_id']

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    if event_name == "item:added" and project_id == project:
        print(timestamp, event_name, event_data['content'])
        api = Sorter(api_token)
        api.capitalize_item(item_id)
        api.learn()
        api.adjust_item_section(item_id)

    if (event_name == "item:completed" or event_name == "item:updated") and str(project_id) == str(project):
        print(timestamp, event_name, event_data['content'])
        api = Sorter(api_token, project_id)
        api.learn()

    return "", 200


@app.route("/", methods=['POST', 'GET'])
def hello():
    return "TodoistSorter service is running..."


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
