from nltk.corpus import stopwords
from typing import List


def remove_stop_words(text: str, lang: str = 'english') -> str:
    """
    Destopping the text.

    text:
    Text from which the stop words are to be removed.

    lang:str='english'
    Language from which the stop words are taken.

    returns:
    Text without the stop words.
    """
    sw = stopwords.words(lang)
    shortened_text = remove_given_stopwords(text, sw)
    return shortened_text


def remove_given_stopwords(text: str, stopwords: List[str] | None = None) -> str:
    """
    Removes the words in the stop word list from the text.

    text:str
    Text to be cleanded. Words are separated by blank spaces.

    stopwords: List[str] | None
    List of words to be removed from the text. if 'None' is passed, the method does nothing
    but returning 'text' itself.

    returns: str
    Stripped text.
    """
    if stopwords is not None:
        shortlist = [word for word in text.split() if word not in stopwords]
        return ' '.join(shortlist)
    else:
        return text
