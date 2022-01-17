# Argumentative Proposition Classifier
![version](https://img.shields.io/badge/version-0.6-blue)
![last-update](https://img.shields.io/badge/last_update-1/17/2022-orange)
![license](https://img.shields.io/badge/license-Apache_2.0-brightgreen)

Implementation of a simple but efficient classifier of argumentative prepositions. The solution is composed of a pipeline of 2 systems, the first one is in charge of automatically extracting the NLP features of each preposition (coming from textual content), and the second one is the classifier which is trained from the output of the first system (features file).

## Dependencies
The implemented solutions depend on or make use of the following libraries:

- Feature extractor (Java solution):
  - JDK 16
  - Stanford CoreNLP 4.2.2
  - MySQL Connector 8.0.22
  - MongoDB Java Driver 3.4.3
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
