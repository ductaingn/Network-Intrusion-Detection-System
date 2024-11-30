'''
Attack Classifier model
'''
# YOUR CODE HERE!
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


class Classifier(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim, mapper):
        '''
        mapper example:
        {
            '0': 'benign',
            '1': 'DDos'
        }
        '''
        super(Classifier, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, output_dim)

        self.mapper = mapper
        self.criterion = nn.CrossEntropyLoss()

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))

        prop = F.softmax(x, dim=0)
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
        # YOUR CODE HERE!
        return
