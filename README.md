# Argumentative Proposition Classifier
![version](https://img.shields.io/badge/version-1.4.0-blue)
![last-update](https://img.shields.io/badge/last_update-10/27/2023-orange)
![license](https://img.shields.io/badge/license-Apache_2.0-brightgreen)

Implementation of a traditional classifier of argumentative components (claims and premises), trained with features/metadata previously extracted from manually annotated argumentative sentences from the citizen proposals available in the <a href="https://decide.madrid.es/" target="_blank">Decide Madrid</a> platform.

The complete solution consists of a pipeline of 6 modules, which are in charge of: data extraction from the source database (Decide Madrid), manual annotation of the data using the <a href="https://github.com/argrecsys/argael" target="_blank">ARGAEL</a> tool (also supports annotations from <a href="https://prodi.gy/" target="_blank">Prodigy</a>), the subsequent feature extraction and the final construction and validation of the feature-based classification models.

## Papers
This work (v1.4) has been accepted as a paper at <a href="https://argmining-org.github.io/2023/">the 10th Workshop on Argument Mining</a> co-located with the 2023 Conference on Empirical Methods in Natural Language Processing (<a href="https://2023.emnlp.org/">EMNLP 2023</a>). A draft of the paper can be found <a href="https://github.com/argrecsys/arg-classifier/tree/main/papers/emnlp23">here</a>.

## Pipeline diagram
![Pipeline diagram](https://raw.githubusercontent.com/argrecsys/arg-classifier/main/image/pipeline-diagram.svg)

Below are links to all datasets (both intermediate and final) created and used by the solution:
- Decide Madrid <a href="https://decide.madrid.es/" target="_blank">platform</a>
- Proposals <a href="https://github.com/argrecsys/arg-classifier/blob/main/data/proposals" target="_blank">JSONL files</a>
- Annotations <a href="https://github.com/argrecsys/arg-classifier/blob/main/data/annotations" target="_blank">CSV files</a>
- Annotated propositions <a href="https://github.com/argrecsys/arg-classifier/blob/main/data/propositions.csv" target="_blank">CSV file</a>
- Features <a href="https://github.com/argrecsys/arg-classifier/blob/main/data/features.json" target="_blank">JSON file</a>
- Labeled dataset <a href="https://github.com/argrecsys/arg-classifier/blob/main/data/dataset.csv" target="_blank">CSV file</a>
- Models results <a href="https://github.com/argrecsys/arg-classifier/blob/main/results/metrics.csv" target="_blank">CSV file</a>

## Dependencies
The implemented solutions depend on or make use of the following libraries:
- Data processor (Python module):
  - python v3.9.13
  - spaCy v3.3.1

- Feature extractor (Java module):
  - JDK 17
  - <a href="https://stanfordnlp.github.io/CoreNLP/" target="_blank">Stanford CoreNLP</a> v4.5.3
  - <a href="https://mongodb.github.io/mongo-java-driver/" target="_blank">MongoDB Java Driver</a> v3.12.10
  - Snake YAML v1.9
  - JSON Java v20210307

- Argument classifier (Python module):
  - python v3.9.13
  - sklearn v0.24.2
  - <a href="https://lightgbm.readthedocs.io/en/latest/" target="_blank">lightgbm</a> v3.3.5
  - <a href="https://www.nltk.org/" target="_blank">nltk</a> v3.6.3
  - <a href="https://optuna.org/" target="_blank">optuna</a> v3.1.1

## Authors
Created on Aug 18, 2021  
Created by:
- <a href="https://github.com/ansegura7" target="_blank">Andrés Segura-Tinoco</a>
- <a href="http://arantxa.ii.uam.es/~cantador/" target="_blank">Iv&aacute;n Cantador</a>

## License
This project is licensed under the terms of the <a href="https://github.com/argrecsys/arg-classifier/blob/main/LICENSE">Apache License 2.0</a>.

## Acknowledgements
This work was supported by the Spanish Ministry of Science and Innovation (PID2019-108965GB-I00).
