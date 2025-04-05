from enum import Enum

class AvailableModels(Enum):
    DISTILBERT_SENTIMENT = ("DistilBERT (Sentiment)", "distilbert-base-uncased-finetuned-sst-2-english")
    BERT_BASE_UNCASED = ("BERT (Base, Uncased)", "bert-base-uncased")
    ROBERTA_BASE = ("RoBERTa (Base)", "roberta-base")
    XLM_ROBERTA_BASE = ("XLM-RoBERTa (Base, Multilingual)", "xlm-roberta-base")
    ALBERT_BASE_V2 = ("ALBERT (Base, v2)", "albert-base-v2")
    DISTILBERT_BASE_UNCASED = ("DistilBERT (Base, Uncased)", "distilbert-base-uncased")
    ELECTRA_SMALL_DISCRIMINATOR = ("ELECTRA (Small Discriminator)", "google/electra-small-discriminator")
    # Add more models as needed

    def __init__(self, display_name, model_value):
        self.display_name = display_name
        self.model_value = model_value

    def to_dict(self):
        return {"name": self.display_name, "value": self.model_value}