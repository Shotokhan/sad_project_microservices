from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from singleton import Singleton
from datetime import timedelta


class App(metaclass=Singleton):
    def __init__(self, module_name="__main__", config_path="./volume/config.json", config=None):
        self.app = Flask(module_name)

        if config is None:
            self.config = {}
            config_path = config_path
            with open(config_path, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = config

        # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////usr/src/app/users.db'
        self.app.config['SQLALCHEMY_DATABASE_URI'] = self.config['db']
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['SECRET_KEY'] = self.config['secret']
        self.app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=self.config['session_validity_days'])
        self.db = SQLAlchemy(self.app)

