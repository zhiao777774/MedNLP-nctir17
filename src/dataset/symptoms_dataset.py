import ast
import pandas as pd
import torch
from types import Dict, List, Tuple
from torch.utils.data import Dataset
from transformers import AutoTokenizer

from utils import search_side_effects


class SymptomsDataset(Dataset):
    def __init__(self,
                 data: pd.DataFrame,
                 targets: List[str],
                 tokenizer: AutoTokenizer,
                 max_len: int,
                 with_drugs: bool = False,
                 top_k: int = 5):
        self.data = data
        self.targets = data[targets].values
        self.tokenizer = tokenizer
        self.max_len = max_len

        self.with_drugs = with_drugs
        self.top_k = top_k

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, idx: int) -> Tuple[Dict[str, torch.Tensor], int]:
        item = self.data.iloc[idx]
        text = item['text']
        input_text = text

        if self.with_drugs:
            drugs = ast.literal_eval(item['drug_name'])
            drug_info = [
                f'{d}:{",".join(search_side_effects(d)["normal"][:self.top_k])}'
                for d in drugs if d != 'None'
            ]
            input_text += ' [SEP] Common side effects of '.join(drug_info)

        concat = self.tokenizer(
            input_text,
            padding='max_length',
            max_length=self.max_len,
            truncation=True,
        )
        concat_ten = {k: torch.tensor(v) for k, v in concat.items()}

        concat_ten['labels'] = torch.tensor(self.targets[idx])

        return concat_ten