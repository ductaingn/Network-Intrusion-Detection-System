'''
Attack Classifier model
'''
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import pandas as pd


class Classifier(nn.Module):
    def __init__(self, input_dim, output_dim, mapper, leaning_rate):
        super(Classifier, self).__init__()
        self.fc1 = nn.Linear(input_dim, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 16)
        self.output = nn.Linear(16, output_dim)

        self.mapper = mapper
        self.criterion = nn.CrossEntropyLoss()
        self.learning_rate = leaning_rate
        self.output_dim = output_dim

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))

        return self.output(x)

    def get_class(self, probability):
        '''
        Get mapped class

        Parameter:
        > probability: model output

        Return class_name

        Example:
        > class_name = ['benign','DDOS','benign'] (len(class_name) = batch_size)

        Hint: use torch.argmax(probability)
        '''
        class_idx = torch.argmax(probability, dim=1)
        class_name = [self.mapper[index.item()+1] for index in class_idx]
        return class_name

    def train_model(self, data:pd.DataFrame, batch_size, epochs, optimizer:optim.Optimizer, save_path):
        '''
        Train model

        Parameter:
        > data: data
        > batch_size: batch size used to train model
        > epochs: number of epochs
        > optimizer: optimizer
        > save_path: path to save model and optimizer state dict

        Return None
        '''
        dataset = IDSDataset(data, self.output_dim)
        train_loader = DataLoader(dataset, batch_size)
        
        self.train()
        for epoch in range(epochs):
            epoch_loss = 0

            for batch_X, batch_y in train_loader:
                optimizer.zero_grad()
                predictions = self(batch_X)
                loss = self.criterion(predictions, batch_y)
                loss.backward()
                optimizer.step()

                epoch_loss += loss.item()
            print("Epoch: {} Loss: {}".format(epoch, epoch_loss))

        try:
            torch.save(
                {
                    'model_state_dict': self.state_dict(),
                    'optimizer_state_dict': optimizer.state_dict(),
                }
                , save_path)

        except Exception as e:
            print('Error occured while trying to save model!')
            print(e)


class IDSDataset(Dataset):
    '''
    Dataset for Classifier model
    '''
    def __init__(self, dataset:pd.DataFrame, output_dim):
        super(IDSDataset, self).__init__()
        self.dataset = dataset
        self.output_dim = output_dim

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, index):
        x = self.dataset.iloc[index, :-self.output_dim].values
        y = self.dataset.iloc[index, -self.output_dim]
    
        return torch.tensor(x, dtype=torch.float32), torch.tensor(y, dtype=torch.long)