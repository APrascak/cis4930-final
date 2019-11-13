#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from google.cloud import firestore
from flask import Flask
database = firestore.Client.from_service_account_json('/Users/Sydney/Desktop/cis4930-final/PINSService/src/pinterestservice-firebase-adminsdk-6ubsp-9e03db19db.json')

def create_app():
    flask_app = Flask(__name__)
    flask_app.app_context().push()
    return flask_app


#
