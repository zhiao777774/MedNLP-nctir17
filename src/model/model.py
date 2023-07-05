import torch.nn as nn
import numpy as np
from transformers import AutoModel


class MultiLabelClassificationModel(nn.Module):
    def __init__(self, model_name, num_classes, n_embs):
        super().__init__()

        self.model = AutoModel.from_pretrained(model_name)
        self.fc = nn.Linear(n_embs, num_classes)

    def forward(self, x):
        _, features = self.model(**x)
        output = self.fc(features)
        return output

    def __str__(self):
        """
        Model prints with number of trainable parameters
        """
        model_parameters = filter(lambda p: p.requires_grad, self.parameters())
        params = sum([np.prod(p.size()) for p in model_parameters])
        return super().__str__() + '\nTrainable parameters: {}'.format(params)