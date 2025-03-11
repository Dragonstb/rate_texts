from rate_texts.dev_tools.story_teller.story_teller import StoryTeller
from rate_texts.dev_tools.story_teller.alg_cat import AlgCat
from typing import Dict
from pathlib import Path
import json

class SampleGenerator():

    config: Dict
    categorizer: AlgCat
    text: str
    """The raw text"""
    html: str
    """The html text"""
    label: int
    """The label assigned to the sample."""

    def __init__(self) -> None:
        self.categorizer = AlgCat()
        # contents = dict()
        # # may raise error
        # path = Path(__file__).parent
        # path = Path(path, 'story_teller/stories.json')
        # if path.exists() and path.is_file():
        #     with open(path, 'rt') as file:
        #         contents = json.load(file)
        # self.config = contents

    def generate_sample(self):
        st = StoryTeller()
        self.text = st.tell_story()
        self.html = '<html><head><title>A story</title><body><p class="text">'+self.text+'</p><p class="end">The End ~</p></body></head></html>'
        self.label = self.categorizer.categotize_text(self.text)

    def get_html(self):
        return self.html

    def get_label(self):
        return self.label
