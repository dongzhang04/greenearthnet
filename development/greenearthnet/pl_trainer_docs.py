#code taken from https://pytorch-lightning.readthedocs.io/en/1.5.10/common/trainer.html
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, random_split
from torchvision.datasets import MNIST
import torchvision.transforms as transforms
import torch.distributed as dist
import os


class MNISTClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer_1 = torch.nn.Linear(28 * 28, 128)
        self.layer_2 = torch.nn.Linear(128, 10)

    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = self.layer_1(x)
        x = F.relu(x)
        x = self.layer_2(x)
        return x


# download data

mnist_train = MNIST(os.getcwd(), train=True, download=True)
mnist_test = MNIST(os.getcwd(), train=False, download=True)

# dist.barrier()

# transforms
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])
mnist_train = MNIST(os.getcwd(), train=True, transform=transform)
mnist_test = MNIST(os.getcwd(), train=False, transform=transform)

# split dataset
mnist_train, mnist_val = random_split(mnist_train, [55000, 5000])
mnist_test = MNIST(os.getcwd(), train=False, download=True)

# build dataloaders
mnist_train = DataLoader(mnist_train, batch_size=64)
mnist_val = DataLoader(mnist_val, batch_size=64)
mnist_test = DataLoader(mnist_test, batch_size=64)
pytorch_model = MNISTClassifier()
optimizer = torch.optim.Adam(pytorch_model.parameters(), lr=1e-3)


def cross_entropy_loss(logits, labels):
    return F.nll_loss(logits, labels)


num_epochs = 1
for epoch in range(num_epochs):
    for train_batch in mnist_train:
        x, y = train_batch
        logits = pytorch_model(x)
        loss = cross_entropy_loss(logits, y)
        print('train loss: ', loss.item())
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

with torch.no_grad():
    val_loss = []
    for val_batch in mnist_val:
        x, y = val_batch
        logits = pytorch_model(x)
        val_loss.append(cross_entropy_loss(logits, y).item())
