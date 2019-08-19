import json
import logging
from typing import Any, Dict, Optional, Text

import requests
from rasa.nlu.extractors import EntityExtractor
from rasa.nlu.training_data import Message

logger = logging.getLogger(__name__)


class ThirdPartyEntityExtractor(EntityExtractor):
    provides = ["entities"]

    requires = ["tokens"]

    def __init__(
            self,
            component_config: Optional[Dict[Text, Any]] = None,
    ) -> None:
        super(ThirdPartyEntityExtractor, self).__init__(component_config)
        self.third_party_service_endpoint = self.component_config.get(
            "third_party_service_endpoint"
        )

    def process(self, message: Message, **kwargs: Any) -> None:
        if self.third_party_service_endpoint is not None:
            headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
            req = requests.post(self.third_party_service_endpoint, data=json.dumps({"text": message.text}), headers=headers)
            extracted = [self.transform_to_extracted(v) for v in req.json() if v["domainType"] != ""]
        else:
            logger.warning(
                "Third party tokenizer component in pipeline, but no "
                "`third_party_service_endpoint` configuration in the config."
            )
            extracted = []
        extracted = self.add_extractor_name(extracted)
        message.set(
            "entities", message.get("entities", []) + extracted, add_to_output=True
        )

    @staticmethod
    def transform_to_extracted(v: Dict[Text, Any]):
        return {
            "start": v["start"],
            "end": v["start"],
            "value": v["text"],
            "entity": v["domainType"],
            "confidence": 1.0,
        }
