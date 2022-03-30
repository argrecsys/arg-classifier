# Argumentative Proposition Classifier
![version](https://img.shields.io/badge/version-0.7.2-blue)
![last-update](https://img.shields.io/badge/last_update-3/30/2022-orange)
![license](https://img.shields.io/badge/license-Apache_2.0-brightgreen)

Implementation of a traditional classifier of argumentative prepositions trained with previously extracted features/metadata and manually annotated argumentative phrases. The solution is composed of a 2-module pipeline, the first one is in charge of automatically extracting the NLP features of each preposition (coming from textual content), and the second one is the classifier that is trained from the output of the first module (specifically, from the features.json file).

## Dependencies
The implemented solutions depend on or make use of the following libraries:

- Feature extractor (Java solution):
  - JDK 16
  - <a href="https://stanfordnlp.github.io/CoreNLP/" target="_blank">Stanford CoreNLP</a> 4.3.1
  - MySQL Connector 8.0.22
  - <a href="https://mongodb.github.io/mongo-java-driver/" target="_blank">MongoDB Java Driver</a> 3.12.10
  - Snake YAML 1.9
  - JSON Java 20210307

- Argument classifier (Python solution):
  - python 3.8.x
  - sklearn 0.24.2
  - nltk 3.6.3

## Authors
Created on Aug 18, 2021  
Created by:
- <a href="https://github.com/ansegura7" target="_blank">Andrés Segura-Tinoco</a>
- <a href="http://arantxa.ii.uam.es/~cantador/" target="_blank">Iv&aacute;n Cantador</a>

## License
This project is licensed under the terms of the <a href="https://github.com/argrecsys/arg-classifier/blob/main/LICENSE">Apache License 2.0</a>.

## Acknowledgements
This work was supported by the Spanish Ministry of Science and Innovation (PID2019-108965GB-I00).
