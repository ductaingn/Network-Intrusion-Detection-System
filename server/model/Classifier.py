'''
Attack Classifier model
'''
import pandas as pd
from sklearn.discriminant_analysis import StandardScaler
from sklearn.model_selection import train_test_split
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

        self.input_dim = input_dim
        self.output_dim = output_dim
        self.mapper = mapper
        self.criterion = nn.BCEWithLogitsLoss()
        self.batch_size = 32

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))

        prop = F.softmax(self.output(x), dim=1)
        return prop

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


    def train_model(self, train_loader, epochs, lr):
        '''
        Train model

        Parameter:
        > train_loader: DataLoader
        > epochs: number of epochs
        > lr: learning rate

        Return None
        '''
        optimizer = optim.Adam(self.parameters(), lr=lr)
        loss_fn = self.criterion
        for epoch in range(epochs):
            self.train()
            epoch_loss = 0
            
            for batch_X, batch_y in train_loader:
                optimizer.zero_grad()
                predictions = self(batch_X)
                loss = loss_fn(predictions, batch_y)
                loss.backward()
                optimizer.step()
                
                epoch_loss += loss.item()
            print(f"Epoch {epoch+1}/{epochs}, Loss: {epoch_loss:.4f}")
                
        torch.save(self.state_dict(), "model/model.pth")

    def load_data(self, path):
        df = pd.read_csv(path)
        X = df.iloc[:, :-self.output_dim]
        y = df.iloc[:, -self.output_dim:]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        y_train = y_train.to_numpy()
        y_test = y_test.to_numpy()

        X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
        X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
        y_train_tensor = torch.tensor(y_train, dtype=torch.float32)
        y_test_tensor = torch.tensor(y_test, dtype=torch.float32)

        self.X_test_tensor = X_test_tensor
        self.y_test_tensor = y_test_tensor
        
        train_data = torch.utils.data.TensorDataset(X_train_tensor, y_train_tensor)
        train_loader = torch.utils.data.DataLoader(train_data, batch_size=self.batch_size, shuffle=True)
        return train_loader
    
    def evaluate(self):
        '''
        Evaluate model

        Return None
        '''
        self.eval()
        with torch.no_grad():
            test_predictions = self(self.X_test_tensor)
            test_predictions = (test_predictions >= 0.5).float()
        
            loss = self.criterion(test_predictions, self.y_test_tensor)
            correct_per_sample = test_predictions.eq(self.y_test_tensor).sum(dim=1)
            total_labels_per_sample = self.y_test_tensor.size(1)
            accuracy_per_sample = correct_per_sample / total_labels_per_sample
            accuracy = accuracy_per_sample.mean().item()
        
            print(f"Loss: {loss:.4f}")
            print(f"F1 Score: {self.f1_score(test_predictions, self.y_test_tensor)}")
            print(f"Accuracy: {accuracy:.4f}")
            