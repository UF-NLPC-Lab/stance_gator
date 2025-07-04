# STL
from typing import Optional
# 3rd Party
from transformers import BartTokenizerFast
# Local
from ..data import SimpleEncoder
from .base_module import StanceModule
from ..models import BartEncForStance, BartEncForStanceConfig

class BartEncModule(StanceModule):

    def __init__(self,
                 pretrained_model: str = 'facebook/bart-large-mnli',
                 classifier_hidden_units: Optional[int] = None,
                 **parent_kwargs):
        super().__init__(**parent_kwargs)
        config = BartEncForStanceConfig.from_pretrained(
            pretrained_model,
            classifier_hidden_units=classifier_hidden_units,
            id2label=self.stance_enum.id2label(),
            label2id=self.stance_enum.label2id(),
        )
        self.wrapped = BartEncForStance.from_pretrained(pretrained_model, config=config)
        self.tokenizer = BartTokenizerFast.from_pretrained(pretrained_model)
        self.__encoder = SimpleEncoder(self.tokenizer)

    @property
    def feature_size(self) -> int:
        return self.wrapped.config.d_model

    def get_optimizer_params(self):
        return [
            {"params": self.wrapped.encoder.parameters(), "lr": 2e-5},
            {"params": self.wrapped.classifier.parameters(), "lr": 1e-3}
        ]
    
    def forward(self, **kwargs):
        return self.wrapped(**kwargs)

    @property
    def encoder(self):
        return self.__encoder