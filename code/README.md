# Solution
The complete solution consists of a pipeline of 6 modules, which are in charge of: data extraction from the source database (Decide Madrid), manual annotation of the data (using the Prodigy tool), the subsequent feature extraction and the final construction and validation of the classification models. Specifically, the modules (Programming Artifacts) are the following: Data Processor, Feature Extractor and Argument Classifier.

### Data Processor
Module in charge of pre-processing the data to convert the output of the Prodigy tool into a valid input for the feature extraction module.
The input parameters (<a href="https://github.com/argrecsys/arg-classifier/blob/main/code/DataProcessor/config/config.json">params.json</a> file) of this module are:
```json
{
	"data_folder": "../../../data/",
	"language": "spanish",
	"task": "preprocessing"
}
```

### Feature Extractor
This module is in charge of automatically extracting the NLP features of each proposition (coming from textual content). It is implemented using Java and CoreNLP library.

The input parameters (<a href="https://github.com/argrecsys/arg-classifier/blob/main/code/FeatureExtractor/Resources/config/params.json">params.json</a> file) of this module are:
```json
{
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
	"data_folder": "../../../data/",
	"language": "spanish",
	"model_folder": "../../../models/",
	"model_state": 42,
	"perc_test": 0.2,
	"result_folder": "../../../results/",
	"task": "detection",
	"y_label": "sent_label2"
}
```

## License
This project is licensed under the terms of the <a href="https://github.com/argrecsys/arg-classifier/blob/main/LICENSE">Apache License 2.0</a>.

## Acknowledgements
This work was supported by the Spanish Ministry of Science and Innovation (PID2019-108965GB-I00).
