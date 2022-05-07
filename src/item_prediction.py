from PIL import Image
import torch
from torch import nn
from torchvision import models, transforms
import matplotlib.pyplot as plt


def get_class_names_dict(filename):
    class_names = {}
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            class_idx = int(line.split(':')[0])
            name = line.split(':')[1]
            name = name[2:-3]
            class_names[class_idx] = name
    return class_names


def get_class_prices_list(filename):
    pass


def img_to_tensor(filename):
    transform = transforms.Compose([
        transforms.Resize((224,224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    img = Image.open(filename).convert('RGB')
    img = transform(img)
    img = img.unsqueeze(0)
    return img


if __name__ == '__main__':

    class_names = get_class_names_dict('class_names.txt')

    img = img_to_tensor('sample_image.jpg')

    model = models.resnet101(pretrained=True)
    model.eval()
    out = model(img)

    _, class_idx = torch.max(out, 1)
    class_idx = class_idx[0].item()

    softmax = nn.Softmax(dim=1)
    out = softmax(out)
    print(out[0, class_idx].item() * 100)
    print(class_names[class_idx])

    # check if image is valid
