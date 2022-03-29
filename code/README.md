# Solution
This solution is composed of a pipeline of 2 modules that mainly perform the following tasks: read and process the input data, extract the features needed to train the models, create and validate the classifier models. Specifically, the modules are the following: Feature Extractor and Argument Classifier.

### Feature Extractor
This module is in charge of automatically extracting the NLP features of each preposition (coming from textual content). It is implemented using Java and CoreNLP library.

### Argument Classifier
This module is the classifier that is trained from the output of the first module (specifically, from the features.json file). It is implemented using Python and Sklearn library.

## License
This project is licensed under the terms of the <a href="https://github.com/argrecsys/arg-classifier/blob/main/LICENSE">Apache License 2.0</a>.

## Acknowledgements
This work was supported by the Spanish Ministry of Science and Innovation (PID2019-108965GB-I00).
