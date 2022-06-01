import uvicorn
from fastapi import FastAPI, File, UploadFile
import io
import os
from PIL import Image
import torch
from torch import nn
from torchvision import models, transforms


def get_dict(filename):
    class_names = {}
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            class_idx = int(line.split(':')[0])
            line = line.split('#')[0] # remove comment
            name = line.split(':')[1]
            name = name[2:-2]
            class_names[class_idx] = name
    return class_names


def preprocessing(img):
    transform = transforms.Compose([
        # transforms.CenterCrop(1000),
        transforms.Resize((224,224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225])
    ])
    img = transform(img)
    img = img.unsqueeze(0)
    return img


def predict(img):
    out = model(img)
    _, class_idx = torch.max(out, 1)
    class_idx = class_idx[0].item()
    softmax = nn.Softmax(dim=1)
    out = softmax(out)

    # print(class_idx)
    class_name = class_names[class_idx]
    percentage = out[0, class_idx].item() * 100
    class_price = class_prices.get(class_idx, 'item is not priced')

    if percentage < 20:
        class_name = 'item is not recognized'

    return {
        'class name': class_name,
        'price': class_price,
        'percentage': percentage,
    }


class_names = get_dict('class_names.txt')
class_prices = get_dict('class_prices.txt')

pretrained = True
if os.path.isfile('resnet101.pt'):
    pretrained = False
model = models.resnet101(pretrained=pretrained)
if pretrained is False:
    model.load_state_dict(torch.load('resnet101.pt'))
model.eval()

app = FastAPI()

@app.post('/')
async def get_info(file: UploadFile = File(...)):
    print(file.filename)

    request_object_content = await file.read()
    img = Image.open(io.BytesIO(request_object_content))
    img.show()

    img = preprocessing(img)
    out = predict(img)
    return out


# if __name__ == '__main__':
    # img = Image.open('sample0.jpg').convert('RGB')
    # img = preprocessing(img)
    # out = predict(img)
    # print(out)
