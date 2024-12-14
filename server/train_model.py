import torch
from model.Classifier import Classifier
from utils import load_config
import yaml

import os

script_dir = os.path.dirname(__file__)
config_path = os.path.join(script_dir, 'configs.json')
model_config_path = os.path.join(script_dir, 'model/model_configs.yaml')

config = load_config(config_path)

with open(model_config_path, 'rb') as file:
    model_config = yaml.safe_load(file)

model = Classifier(
    model_config['architecture']['input_dim'], 
    model_config['architecture']['output_dim'], 
    model_config['mapper'])

data_path = os.path.join(script_dir, 'model/train_data.csv')
train_loader = model.load_data(data_path)

epochs = 50
learning_rate = 0.001
model.train_model(train_loader, epochs, learning_rate)
