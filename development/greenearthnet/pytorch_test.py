import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""
import torch
# print(torch.__version__)
# print(torch.__config__.show())
# print(torch.version.cuda) 
# print(torch.backends.cudnn.version())
# if torch.cuda.is_available():
#     x = torch.randn(3, 3, device="cuda", requires_grad=True)
#     y = (x ** 2).sum()
#     y.backward()
#     print("CUDA autograd works")
import torch.nn as nn
import torch.optim as optim

# Simple test model
class TestModel(nn.Module):
    def __init__(self):
        super(TestModel, self).__init__()
        self.fc = nn.Linear(10, 1)

    def forward(self, x):
        return self.fc(x)

def run_test(device):
    print(f"\nRunning on: {device}")
    model = TestModel().to(device)
    criterion = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=0.01)

    # Random input/output tensors
    x = torch.randn(16, 10, device=device)
    y = torch.randn(16, 1, device=device)

    # One training step
    optimizer.zero_grad()
    outputs = model(x)
    print("inference step complete")
    loss = criterion(outputs, y)
    print("beginning loss.backward")
    loss.backward()
    print("loss.backward passed")
    optimizer.step()

    print(f"Finished one training step on {device}, loss = {loss.item():.4f}")

if __name__ == "__main__":
    # Always works
    run_test("cpu")

    # Only run if CUDA is available
    # print(torch.cuda.get_device_name(0))
    if torch.cuda.is_available():
        run_test("cuda")
    else:
        print("\nCUDA not available on this machine.")
