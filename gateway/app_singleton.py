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

        self.gestioneUtentiURL = "http://{}:{}".format(
            self.config['gestione_utenti_ip'], self.config['gestione_utenti_port']
        )
        self.gestionePrenotazioniURL = "http://{}:{}".format(
            self.config['gestione_prenotazioni_ip'], self.config['gestione_prenotazioni_port']
        )
