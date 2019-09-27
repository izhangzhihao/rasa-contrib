# Welcome to rasa-contrib

## This Repository

This repository stores third party components used by the developer community.

* third_party_extractor.py - third party http conponent for extractor.
* third_party_tokenizer.py - third party http conponent for tokenizer.

## Usage

config.yml

```yml
language: en
pipeline:
  - name: "third_party_tokenizer.ThirdPartyTokenizer"
    third_party_service_endpoint: http://tokenize-api/tokenize
    type: tokenizer
  - name: "RegexFeaturizer"
  - name: "third_party_extractor.ThirdPartyEntityExtractor"
    third_party_service_endpoint: http://tokenize-api/tokenize
    type: extractor
  - name: "EntitySynonymMapper"
  - name: "CountVectorsFeaturizer"
  - name: "EmbeddingIntentClassifier"
...
```
