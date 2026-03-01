import torch
import torchvision.transforms as transforms
from PIL import Image
from model import CNN
from classes import class_names

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = CNN(len(class_names))
model.load_state_dict(torch.load("model.pth", map_location=device))
model.to(device)
model.eval()

transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
])

def predict_image(img_path):
    image = Image.open(img_path).convert("RGB")
    image = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(image)
        probabilities = torch.softmax(outputs, dim=1)
        confidence, predicted = torch.max(probabilities, 1)

    disease = class_names[predicted.item()]
    confidence = round(confidence.item() * 100, 2)

    return disease, confidence