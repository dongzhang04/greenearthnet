# import os
# os.environ["CUDA_VISIBLE_DEVICES"] = ""
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset
import pytorch_lightning as pl

print("test starting")

X = torch.randn(500, 10)
y = torch.randint(0, 2, (500,))
dataset = TensorDataset(X, y)
dataloader = DataLoader(dataset, batch_size=32)

print("dataset created")

class SimpleClassifier(pl.LightningModule):
    def __init__(self):
        super().__init__()
        self.layer = nn.Linear(10, 2)

    def forward(self, x):
        return self.layer(x)

    def training_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = F.cross_entropy(logits, y)
        self.log("train_loss", loss, prog_bar=True)
        return loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=1e-3)

print("before torch.cuda call")
print("CUDA available:", torch.cuda.is_available())
print("after torch.cuda call")

# for accelerator, devices in [("cpu", 1), ("gpu", 1)]:
    # print(f"Testing Trainer(accelerator='{accelerator}', devices={devices})")
    # model = SimpleClassifier()
    # trainer = pl.Trainer(
    #     accelerator=accelerator,
    #     devices=devices,
    #     max_epochs=2,
    #     log_every_n_steps=1,
    # )
    # trainer.fit(model, dataloader)
    # print(f"Trainer on {accelerator} ran successfully")

print(f"Testing Trainer(accelerator = cpu, devices = auto)")
model = SimpleClassifier()
trainer = pl.Trainer(
    accelerator="cpu",
    devices="auto",
    max_epochs=2,
    log_every_n_steps=1,
)
print("Trainer instantiated")
trainer.fit(model, dataloader)
print(f"Trainer on cpu ran successfully")

print("end")