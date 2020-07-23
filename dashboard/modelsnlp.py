from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu import config
from rasa_nlu.model import Metadata, Interpreter
import pickle
import os

global_data =''

def load_and_train():
    print(os.path.abspath(__file__))
    train_data  = load_data('dashboard/rasa_data_servers.json')
    trainer = Trainer(config.load('dashboard/config_spacy.yaml'))
    trainer.train(train_data)
    model_directory = trainer.persist('dashboard/projects')
    interpreter = Interpreter.load(model_directory)
    global global_data
    global_data =interpreter
    return interpreter



def get_globalcallls():
    global global_data
    global_data = 25
