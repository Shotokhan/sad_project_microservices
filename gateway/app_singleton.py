from flask import Flask
import json
from singleton import Singleton


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

        self.gestioneUtentiURL = self.config['gestione_utenti_url']
        self.gestionePrenotazioniURL = self.config['gestione_prenotazioni_url']
