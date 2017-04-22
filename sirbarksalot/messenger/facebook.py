from flask import Flask, request, jsonify
import requests
import json
import traceback
import os
TOKEN = os.environ["FACEBOOK_TOKEN"]
URL = "https://graph.facebook.com/v2.6/me/messages?access_token={}".format(TOKEN)

def parse_post(request_data):
    data = json.loads(request_data)
    print data
    _message = data['entry'][0]['messaging'][0]
    text, sender = _message['message']['text'], _message['sender']['id']
    payload = {
        'recipient': {'id': sender},
        'message': {'text': 'woof woof'}
    }
    headers = {'Content-Type': 'application/json'}
    print payload
    requests.post(URL, json=payload, headers=headers)
    return "Message sent"

def verify(args):
    if args.get('hub.verify_token') == 'cody_barks_alot':
        return args.get('hub.challenge')
    return "Wrong Verify Token"

def webhook():
    if request.method == 'POST':
        try:
            return parse_post(request.data)

        except Exception as e:
            print traceback.format_exc()

    elif request.method == 'GET':
        return verify(request.args)

def create_app():
    app = Flask(__name__)
    app.add_url_rule('/webhook', view_func=webhook, methods=['GET', 'POST'])
    return app
