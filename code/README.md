# Solution
The complete solution consists of a pipeline of 6 modules, which are in charge of: data extraction from the source database (Decide Madrid), manual annotation of the data using the <a href="https://github.com/argrecsys/argael" target="_blank">ARGAEL</a> tool (also supports annotations from <a href="https://prodi.gy/" target="_blank">Prodigy</a>), the subsequent feature extraction and the final construction and validation of the feature-based classification models. Specifically, the modules (Programming Artifacts) are the following: Data Processor, Feature Extractor and Argument Classifier.

### Data Processor
Module in charge of pre-processing the data to convert the output of the ARGAEL (or Prodigy) tool into a valid input for the feature extraction module.
The input parameters (<a href="https://github.com/argrecsys/arg-classifier/blob/main/code/DataProcessor/config/config.json">config.json</a> file) of this module are:
```json
{
	"anno_tool": "argael",   // or prodigy
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
	"features": {
		"remove_stopwords": true,
		"bow_unigrams": true,
		"bow_bigrams": false,
		"bow_trigrams": false,
		"pos_unigrams": true,
		"pos_bigrams": false,
		"word_couples": false,
		"entities": true,
		"adverbs": true,
		"verbs": true,
		"nouns": true,
		"modal_auxs": true,
		"punctuation": true,
		"key_words": true,
		"struc_stats": true,
		"synt_stats": true
	},
	"pipeline": {
		"data_scale_algo": "normalize",   // standardize
		"dim_red_algo": "pca",            // lda
		"ml_algo": "gradient-boosting"    // logistic-regression, naive-bayes, support-vector-machine
	},
	"train": {
		"cv_k": 10,
		"cv_stratified": true,
		"model_state": 42,
		"perc_test": 0.2
	},
	"create_dataset": true,
	"data_folder": "../../../data/",
	"language": "spanish",
	"model_folder": "../../../models/",
	"result_folder": "../../../results/",
	"task": "detection",                  // classification
	"y_label": "sent_label1"              // sent_label2
}
```

## License
This project is licensed under the terms of the <a href="https://github.com/argrecsys/arg-classifier/blob/main/LICENSE">Apache License 2.0</a>.

## Acknowledgements
This work was supported by the Spanish Ministry of Science and Innovation (PID2019-108965GB-I00).
