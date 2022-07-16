from torch.utils.data import Dataset, DataLoader
import pandas as pd
import os
import torchvision.transforms as transforms
from torchvision.models import inception_v3
import torch
from PIL import Image
from retinaDataset import *
from tqdm import tqdm

pd.read_csv("../input/diabetic-retinopathy-resized/trainLabels.csv")['level'].unique()
cropped = pd.read_csv("../input/diabetic-retinopathy-resized/trainLabels_cropped.csv")[:5000]


def train_model():
    learning_rate = 1e-4
    num_epochs = 1
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    my_transform = transforms.Compose([transforms.Resize((299,299)),transforms.ToTensor()])
    train_dataset = retinaDataset(total=5000)
    model = inception_v3(pretrained=True)

    for param in model.parameters():
        param.requires_grad = False
        
    model.fc = torch.nn.Linear(in_features=2048, out_features=5, bias=True)

    model.aux_logits = False

    model = model.to(device=device)

    optimizer = torch.optim.Adam(model.parameters(), lr = learning_rate)
    loss_criterion = torch.nn.CrossEntropyLoss()
    train_dataloader = DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)


    for epoch in range(num_epochs):
        for data, target in tqdm(train_dataloader):
            data = data.to(device=device)
            target = target.to(device=device)
            
            score = model(data)
            optimizer.zero_grad()
            
            loss = loss_criterion(score, target)
            loss.backward()
            
            optimizer.step()
        
        print(f"for epoch {epoch}, loss : {loss}")

    for epoch in range(num_epochs):
        for data, target in tqdm(train_dataloader):
            data = data.to(device=device)
            target = target.to(device=device)
            
            score = model(data)
            optimizer.zero_grad()
            
            loss = loss_criterion(score, target)
            loss.backward()
            
            optimizer.step()
        
        print(f"for epoch {epoch}, loss : {loss}")
    
    return model

def check_accuracy(model, loader):
        model.eval()
        correct_output = 0
        total_output = 0
            
        with torch.no_grad():
            for x, y in tqdm(loader):
                x = x.to(device=device)
                y = y.to(device=device)
                
                score = model(x)
                _,predictions = score.max(1)
                
                correct_output += (y==predictions).sum()
                total_output += predictions.shape[0]
        model.train()
        print(f"out of {total_output} , total correct: {correct_output} with an accuracy of {float(correct_output/total_output)*100}")


model = train_model()
check_accuracy(model, train_dataloader)
