# Solution
This solution is composed of a pipeline of 2 modules that mainly perform the following tasks: read and process the input data, extract the features needed to train the models, create and validate the classifier models. Specifically, the modules are the following: Feature Extractor and Argument Classifier.

### Feature Extractor
This module is in charge of automatically extracting the NLP features of each preposition (coming from textual content). It is implemented using Java and CoreNLP library.

The input parameters (<a href="https://github.com/argrecsys/arg-classifier/blob/main/code/FeatureExtractor/Resources/config/params.json">params.json</a> file) of this module are:
```json
{
    "customProposalID": [7, 19, 50, 61, 72, 86, 89, 109, 152, 417],
    "createDataset": true,
    "extractionMode": "detection",
    "language": "es",
    "linkers": {
        "en": {
            "invalidAspects": ["also", "thing", "mine", "sometimes", "too", "other"],
            "invalidLinkers": ["and", "or"],
            "validLinkers": []
        },
        "es": {
            "invalidAspects": ["tambien", "cosa", "mia", "veces", "ademas", "demas"],
            "invalidLinkers": ["o", "y"],
            "validLinkers": []
        }
    }
}
```

### Argument Classifier
This module is the classifier that is trained from the output of the first module (specifically, from the features.json file). It is implemented using Python and Sklearn library.

The input parameters (<a href="https://github.com/argrecsys/arg-classifier/blob/main/code/ArgumentClassifier/config/config.json">config.json</a> file) of this module are:
```json
{
    "data": {
        "force_create": true,
		"remove_stopwords": true,
		"punctuation": true,
		"unigrams": true,
		"bigrams": false,
		"trigrams": false,
		"word_couples": false,
		"adverbs": true,
		"verbs": true,
		"key_words": true,
		"text_stats": true
	},
	"language": "spanish",
	"model_folder": "../../../model/",
	"model_state": 42,
	"output_folder": "../../../dataset/",
	"perc_test": 0.2,
	"result_folder": "../../../result/",
	"task": "identification",
	"y_label": "category"
}
```

## License
This project is licensed under the terms of the <a href="https://github.com/argrecsys/arg-classifier/blob/main/LICENSE">Apache License 2.0</a>.

## Acknowledgements
This work was supported by the Spanish Ministry of Science and Innovation (PID2019-108965GB-I00).
