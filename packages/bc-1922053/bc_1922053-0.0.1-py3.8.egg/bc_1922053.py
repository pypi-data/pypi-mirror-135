import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
import numpy as np
import matplotlib.pyplot as plt

import time

device = 'cuda' if torch.cuda.is_available() else 'cpu'

transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(), 
    transforms.Normalize((0.5,), (0.5,)),
])

train_dataset = datasets.ImageFolder('/Users/acht0714/bc/src/a/train', transform=transform)
val_dataset = datasets.ImageFolder('/Users/acht0714/bc/src/a/val', transform=transform)

train_loader = DataLoader(train_dataset, batch_size=128, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=128, shuffle=False)

data_iter = iter(train_loader)
imgs, labels = data_iter.next()

plt.imshow(imgs[0].permute(1,2,0))

model = models.resnet18(pretrained=True)

for param in model.parameters():
  param.requires_grad = False

model.fc = nn.Linear(in_features=512, out_features=2, bias=True)

model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

num_epochs = 10
train_loss_list = []
train_acc_list = []
val_loss_list = []
val_acc_list = []

for epoch in range(num_epochs):
    train_loss = 0
    train_acc = 0
    val_loss = 0
    val_acc = 0

    #学習プロセス
    model.train()

    for i, (images, labels) in enumerate(train_loader):

        images = images.to(device)
        labels = labels.to(device)
      
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)

        train_loss += loss.item()
        pred = torch.argmax(outputs, dim=1)
        train_acc += (pred == labels).sum().item()

        loss.backward()
        optimizer.step()
        
    avg_train_loss = train_loss / len(train_loader.dataset)
    avg_train_acc = train_acc / len(train_loader.dataset)
    
    #検証プロセス
    model.eval()
    with torch.no_grad():
      for images, labels in val_loader:
          
          images = images.to(device)
          labels = labels.to(device)

          outputs = model(images)
          loss = criterion(outputs, labels)
          
          val_loss += loss.item()
          pred = torch.argmax(outputs, dim=1)
          val_acc += (pred == labels).sum().item()

    avg_val_loss = val_loss / len(val_loader.dataset)
    avg_val_acc = val_acc / len(val_loader.dataset)
        
    print ('Epoch [{}/{}], Loss: {loss:.4f}, val_loss: {val_loss:.4f}, val_acc: {val_acc:.4f}' 
                   .format(epoch+1, num_epochs, i+1, loss=avg_train_loss, val_loss=avg_val_loss, val_acc=avg_val_acc))
    train_loss_list.append(avg_train_loss)
    train_acc_list.append(avg_train_acc)
    val_loss_list.append(avg_val_loss)
    val_acc_list.append(avg_val_acc)



from PIL import Image

image_file_path = '/Users/acht0714/bc/src/a/no_2 (1).png'

img = Image.open(image_file_path)
img_transformed = transform(img)
img_transformed.size()
inputs = img_transformed.unsqueeze_(0)
inputs.size()
outputs = model(inputs)
pred = torch.argmax(outputs, dim=1)

if pred == 0:
    print('ユニクロ')
elif pred == 1:
    print('Noid')
