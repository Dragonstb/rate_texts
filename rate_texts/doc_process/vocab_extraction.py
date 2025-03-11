from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


def extract_vocab(docs: List[str], min_df=1, ngram_range: Tuple[int, int] = (1, 1), threshold: float = 0.98, verbose: bool = True, skip_dropping: bool = False):
    """
    Extracts the vocabulary from the list of documents. The appearance or non appearance of the
    words from this vocabulary in a document are the features that are eventually analyzed.

    In the standard settings, the algorithm checks the correlation of the apearances of each pair of words.
    If the appearance of two words across all documents correlates or anticorrelates with each other, one
    of the words is dropped from the vocabulary.

    docs: List[str]
    The documents.

    min_df (default 1):
    A word is omitted for the vocabulary if it appears in less documents than this value is set to.

    ngram_range: Tuple[int, int] = (1,1)
    The n-grams that make up the vocabulary.

    threshold: float = 0.98:
    If the magnitude of the correlation between the document appearance vectors of two words exceeds
    this threshold, one of the two words is dropped from the vocabulary.

    verbose: bool = True:
    If and only if, a progress indicator is printed to sout.

    skip_dropping: bool = False:
    Determines if the dropping of words thats appearance strongly (anti)correlates with another words
    shall be omitted.
    """
    vect = TfidfVectorizer(min_df=min_df, use_idf=False,
                           binary=True, norm=None, ngram_range=ngram_range)

    print_to_console(verbose, 'getting vocab', end='')
    matrix = vect.fit_transform(docs)
    vocab = vect.get_feature_names_out()

    droplist = []

    for word in range(len(vocab)-1):
        print_to_console(
            verbose, f'\rchecking word {word+1} of {len(vocab)-1}, dropped {len(droplist)} words so far', end='')
        if word in droplist:
            continue

        x = matrix.getcol(word).toarray().T[0]
        if np.min(x) >= 1:
            # word appears in all documents
            droplist.append(word)
            continue

        for other in range(word+1, len(vocab)):
            if other in droplist:
                continue
            # check if (almost) all values in an array are the same
            # values in x and z are either floats of 0 or 1. We can assume a strong correlation
            # when x and z are the same in most positions
            z = matrix.getcol(other).toarray().T[0]
            same_values_at = np.abs(x-z) < .1
            if len(x[same_values_at]) / len(x) > threshold:
                droplist.append(other)

    print_to_console(verbose)  # new line in console

    arr = np.array([True for _ in range(len(vocab))])
    arr[droplist] = False

    shortlist = vocab[arr]
    return shortlist


def print_to_console(verbose: bool, text: str = '', end: str | None = None) -> None:
    if verbose:
        print(text, end=end) if end is not None else print(text)
