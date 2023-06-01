import torch
import torchtext
from transformers import LongformerTokenizer, LongformerConfig, LongformerModel


class Model(torch.nn.Module):
    def __init__(self, num_labels):
        super().__init__()
        self.transformer = LongformerModel(
            LongformerConfig.from_pretrained("allenai/longformer-base-4096")
        )
        self.output = torch.nn.Linear(in_features=768, out_features=num_labels)
        self.sigmoid = torch.nn.Sigmoid()

    def forward(self, input_ids=None, attention_mask=None):
        x = self.transformer(input_ids=input_ids, attention_mask=attention_mask)[
            "pooler_output"
        ]  # "pooler_output", "last_hidden_state"
        x = self.output(x)
        x = self.sigmoid(x)
        return x


class Classifier:
    def __init__(self, model_path, tokenizer_path, vocab_path, device=None):
        self.vocab = torch.load(vocab_path)
        self.tokenizer = LongformerTokenizer.from_pretrained(
            "allenai/longformer-base-4096"
        )
        self.model = Model(len(self.vocab))

        self.model.load_state_dict(torch.load(model_path))
        self.model.eval()

        if device:
            pass
        elif torch.cuda.is_available():
            device = "cuda"
        else:
            device = "cpu"

        self.device = torch.device(device)

    def classify(self, texts):
        inputs = self.tokenizer(
            texts, padding="max_length", truncation=True, return_tensors="pt"
        )

        with torch.no_grad():
            probabilities = self.model(**inputs)

        print(probabilities)
        labels = self._decode_labels((probabilities > 0.4).to(int))

        return labels

    def _decode_labels(self, x):
        x = [torch.flatten(row.nonzero()).tolist() for row in x]
        x = [self.vocab.lookup_tokens(row) for row in x]
        return x
