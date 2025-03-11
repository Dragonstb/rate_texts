from typing import Tuple, DefaultDict, List
from rate_texts.dev_tools.story_teller.story_teller import StoryTeller
import re
from random import random

class AlgCat:
    """Algorithmically categorizes the texts produced by the story teller."""

    _GOOD = 'positive indicators'
    _VERY_GOOD = 'very positive indicators'
    _BAD = 'negative indicators'
    _VERY_BAD = 'very negative indicators'
    _GOOD_BASE = 'positive base'
    _BAD_BASE = 'negative base'
    reasons: DefaultDict[str, List[str]]
    base_level: int
    pos_influence: int
    neg_influence: int
    variation: int

    def categotize_text(self, original_text: str) -> int:
        self.reasons = DefaultDict()
        self.reasons[self._GOOD] = []
        self.reasons[self._VERY_GOOD] = []
        self.reasons[self._BAD] = []
        self.reasons[self._VERY_BAD] = []
        self.reasons[self._GOOD_BASE] = []
        self.reasons[self._BAD_BASE] = []

        text = original_text.lower()
        level = self._get_base_level(text)
        pos, neg = self._get_influences(text)
        mean = .5*(pos+neg)
        diff = abs(pos-neg)

        self.base_level = level
        self.pos_influence = pos
        self.neg_influence = neg
        
        # variate base level by
        var = 0
        if diff > .6 * mean and mean > 1.8:
            var = 2 if pos > neg else -2
        elif diff > .3 * mean:
            var = 1 if pos > neg else -1
        self.variation = var

        # variate base level
        level = level + var
        
        # clamp level
        if level > 5:
            level = 5
        elif level < 0:
            level = 0

        return level

    def _get_influences(self, text: str) -> Tuple[int, int]:
        # Alex likes fantasy, magic and when someone has to be rescued. Also, mountains are Alex' favourite landscape.
        # There are also some names Alex like
        good = ['wizard', 'witch', 'mage', 'spell', 'kidnapped', 'mountain', 'mountains', 'valley', 'valleys']

        # and especially dragons
        very_good = ['dragon']

        # Alex somewhat dislikes detective stories and shootings. Forests disgust Alex.
        bad = ['pi', 'shooting', 'shootout', 'forest', 'forests', 'wood', 'woods', 'rain', 'rainy']

        # and definitely dislikes fire
        very_bad = ['fire']

        positives = 0
        negatives = 0
        for word in good:
            if re.search(r'\W'+word+r'\W', text) != None:
                positives = positives + 1
                self.reasons[self._GOOD].append(word)
        for word in very_good:
            if re.search(r'\W'+word+r'\W', text) != None:
                positives = positives + 2
                self.reasons[self._VERY_GOOD].append(word)
        for word in bad:
            if re.search(r'\W'+word+r'\W', text) != None:
                negatives = negatives + 1
                self.reasons[self._BAD].append(word)
        for word in very_bad:
            if re.search(r'\W'+word+r'\W', text) != None:
                negatives = negatives + 2
                self.reasons[self._VERY_BAD].append(word)
        return (positives, negatives)

    def _get_base_level(self, text: str) -> int:
        # Alex prefers good endings over bad endings
        last_sentence = self._extract_last_sentence(text)
        good = ['happy', 'happily']
        bad = ['died', 'dead']
        base_level = 2
        for word in bad:
            if re.search(r'\W'+word+r'\W', last_sentence) != None:
                base_level = 1
                self.reasons[self._BAD_BASE].append(word)
                break
        for word in good:
            # 'good' can overwrite 'bad'
            if re.search(r'\W'+word+r'\W', last_sentence) != None:
                base_level = 3 if random() < .5 else 4
                self.reasons[self._GOOD_BASE].append(word)
                break
        return base_level

    def _extract_last_sentence(self, text: str) -> str:
        idx_last_full_stop = text.rfind('.')
        idx_penultimate_full_stop = text[:idx_last_full_stop].rfind('.')
        last_sentence = text[idx_penultimate_full_stop+1:idx_last_full_stop].strip()
        return last_sentence

def make_statistics(size: int = 1000) -> None:
    levels = DefaultDict()
    for level in range(6):
        levels[level] = 0

    variations = DefaultDict()
    for var in [x-2 for x in range(5)]:
        variations[var] = 0

    ag = AlgCat()
    print(f'Text 1 of {size}', end='')
    for counter in range(size):
        if (counter+1) % 50 == 0:
            print(f'\rText {counter+1} of {size}', end='')
        st = StoryTeller()
        text = st.tell_story()
        level = ag.categotize_text(text)
        levels[level] = levels[level] + 1
        var = ag.variation
        variations[var] = variations[var] + 1
    
    print()
    print('levels:')
    for key in levels.keys():
        fraction = round(100*levels[key]/size)
        print(f'{str(key)}: {levels[key]}\t{fraction}%')

    print()
    print('Variations:')
    for key in variations.keys():
        fraction = round(100*variations[key]/size)
        print(f'{str(key)}: {variations[key]}\t{fraction}%')

if __name__ == '__main__':
    st = StoryTeller()
    text = st.tell_story()
    ag = AlgCat()
    level = ag.categotize_text(text)
    print()
    print(text)
    print()
    print('\tThe End ~')
    print()
    print(f'Category: {level}')
    print(f'Base level: {ag.base_level}')
    print(f'Positive influence level: {ag.pos_influence}')
    print(f'Negative influence level: {ag.neg_influence}')
    print(f'Variation level: {ag.variation}')
    print()
    for key in ag.reasons.keys():
        print(f'{key}: {ag.reasons[key]}')
    print()
