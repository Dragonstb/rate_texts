# *rate_texts*

A python module for rating text content based on a machine learning model.

A word of warning: this project is still under initial development. It might be not that usable yet as it is going to be once it leaves the initial phase.

## Scope

This module rates how interesting a text, provided by an html document, is for you, from zero to five starts, once you have trained an AI model. The main assumption is that your rating of a text purely raises from the appearance and the non-appearance of certain words in the document. This ansatz might be true for short texts that intend to point out certain aspects, maybe like recipes (chocolate and raisins are tasty but garlic and salmon in a cake recipe might be not).

*rate_texts* helps you managing the data that comes with the task. The module keeps track of the sample files and their meta data. Such meta data might be language, if it is used as a sample for training, or the actual rating.

The same way you can store, organize and use different models. The module also lists them together with their training and tests scores. You can set up one or more models and add them to the framework. Currently, the module can handle tensorflow/keras models and scikit-learn models. Wrapper provide a common interface for the different models.

The module *rate_texts* also prepares the raw text files. For now, these documents need to be html files. *rate_texts* strips away the html from the texts, removes the stop words using [nltk](https://www.nltk.org/), and stems the remaining words with the [snowballstemmer](https://pypi.org/project/snowballstemmer/). From the prepared texts a vocabulary is generated using the [scikit-learn TfidfVectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html). Words that appear in all documents or that correlate very strongly in their appearances with other words can optionally be dropped from the vocabulary.

## Usage

The data can be easily accessed, processed and manipulated directly from the python console. For this purpose, a lot of convenience methods are provided by an instance of the class rate_texts.core.rate_texts.RateTexts. In Future, there might be an even more user friendly CLI tool and a GUI tool.

For testing models, a test project can be created by a single command. In this test project, a whole bunch of fictional, short stories are generated by a, very simple, story generator and become labeled algorithmically.



### Instruction manual

**1 Create an instance of RateTexts**

In your pthon console:

```
from rate_texts.core.rate_texts import RateTexts
import pandas as pd

rate = RateTexts()
```

This oject offers the commands you need.

**2 Create a new project**

```
rate.create_project("my_project")
```

This creates a folder "my_project" in the configured home folder of rate_texts, alongside all necessary subfolders.

For a quick start, you can type `rate.make_dev_project(1234, 'MyStartProject')` into the console instead. This creates a new project "MyStartProject" (change name to whatever you want) and populates the training data with 1234 samples (you can change the number at your will). The samples are generated by an algorithmic story teller and labeled by an algorithmic categorizer. Don't expect the story teller to win the Nobel prize for literature, though.

**3 Fill the training folder with the training data**

The html files for training (and testing) go to `my_project/training/<any subdirectory>`.



**4 Update the file index for the training data**

By a call of

```
df = rate.update_project()
```

all subdirectories in `my_project/training/` are browsed for html files (.htm, .html). A
pandas DataFrame is created or updated with the samples yet not listed. This data frame is
both returned by the method and stored into `my_project/training/document_index.csv`.

**5 Preprocess your samples**

We do not want to do the natural language processing (NLP) on html files. The files have to be cleaned from html code.
Also, usual NLP tasks like the removal of stopwords and the stemming of the remaining words must be done.

To do so, enter

```
rate.prepare_unclean_samples()
```
