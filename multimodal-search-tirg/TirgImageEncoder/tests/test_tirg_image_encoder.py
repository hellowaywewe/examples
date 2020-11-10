__copyright__ = "Copyright (c) 2020 Jina AI Limited. All rights reserved."
__license__ = "Apache-2.0"

import os

import torch
import pytest
import numpy as np
import torchvision
from PIL import Image

from .. import TirgImageEncoder

cur_dir = os.path.dirname(os.path.abspath(__file__))

@pytest.fixture
def transformer():
    return torchvision.transforms.Compose([
        torchvision.transforms.Resize(224),
        torchvision.transforms.CenterCrop(224),
        torchvision.transforms.ToTensor(),
        torchvision.transforms.Normalize([0.485, 0.456, 0.406],
                                         [0.229, 0.224, 0.225])])


def test_image_embeddings(transformer):
    imgs = []
    for img_name in range(3):
        img_path = os.path.join(cur_dir, f'imgs/{img_name}.jpeg')
        with open(img_path, 'rb') as f:
            img = Image.open(img_path)
            img = img.convert('RGB')
            img = transformer(img)
            imgs.append(img)
    encoder = TirgImageEncoder(
        model_path='checkpoint_fashion200k.pth',
        texts_path='texts.pkl',
        channel_axis=1,
    )
    imgs = torch.stack(imgs).float()
    embeddings = encoder.encode(imgs.numpy())
    expected = np.load(os.path.join(cur_dir, 'expected.npy'))
    np.testing.assert_almost_equal(embeddings, expected)
