import pandas as pd
import torch
from model.Classifier import Classifier
from utillities import load_config
import yaml

import os

script_dir = os.path.dirname(__file__)
config_path = os.path.join(script_dir, 'configs.json')
model_config_path = os.path.join(script_dir, 'model/model_configs.yaml')
model_save_path = os.path.join(script_dir, 'model/model.pth')

config = load_config(config_path)

with open(model_config_path, 'rb') as file:
    model_config = yaml.safe_load(file)

model = Classifier(
    model_config['architecture']['input_dim'], 
    model_config['architecture']['output_dim'], 
    model_config['mapper'],
    model_config['learning_rate'])

data_path = os.path.join(script_dir, 'model/train_data.csv')
dataset = pd.read_csv(data_path)

epochs = 200
learning_rate = 0.001
model.train_model(dataset, batch_size=32, epochs=epochs, 
                  optimizer=torch.optim.Adam(model.parameters(), lr=model.learning_rate), 
                  save_path=model_save_path)
