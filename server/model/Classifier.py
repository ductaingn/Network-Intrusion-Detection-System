'''
Attack Classifier model
'''
# YOUR CODE HERE!
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


class Classifier(nn.Module):
    def __init__(self, input_dim, output_dim, mapper):

        super(Classifier, self).__init__()
        self.fc1 = nn.Linear(input_dim, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 16)
        self.output = nn.Linear(16, output_dim)

        self.mapper = mapper
        self.criterion = nn.BCEWithLogitsLoss()

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))

        prop = F.softmax(x, dim=1)
        return prop, self.get_class(prop)

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


    def train(self, train_loader, epochs, lr):
        '''
        Train model

        Parameter:
        > train_loader: DataLoader
        > epochs: number of epochs
        > lr: learning rate

        Return None
        '''
        optimizer = optim.Adam(self.parameters(), lr=lr)
        for epoch in range(epochs):
            self.train()
            epoch_loss = 0
            
            for batch_X, batch_y in train_loader:
                optimizer.zero_grad()
                predictions = self(batch_X)
                loss = self.criterion(predictions, batch_y)
                loss.backward()
                optimizer.step()
                
                epoch_loss += loss.item()
                
        F.save(self.state_dict(), "path/to/model.pth")
