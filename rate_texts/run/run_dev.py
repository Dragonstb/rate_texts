from pathlib import Path
from rate_texts.run import run_gen
import pandas as pd
from rate_texts.dev_tools.sample_generator import SampleGenerator as SG
from rate_texts.doc_process import html_cleaning, stops_removal, stemming, vocab_extraction
from sklearn.model_selection import train_test_split
from rate_texts.core.project import Project
from rate_texts.tools import keys


def create_dev_project(size: int, name: str, parent: Path) -> Project:
    prj = run_gen.create_project_folders(name, parent)
    sg = SG()
    cols = []
    file_data = []
    docs = []
    successes = 0
    train_dir = Path(prj.root_dir, prj.training_dir).absolute()
    print('writing to '+str(train_dir))

    print(f'generating sample 1 of {size}', end='')
    counter = 0
    lang = 'english'
    for _ in range(size):
        counter = counter + 1
        if counter % 50 == 0:
            print(f'\rgenerating sample {counter} of {size}', end='')

        # generate labeled sample
        sg.generate_sample()

        # extract data from sample
        html = sg.get_html()
        rating = sg.get_label()
        sample_id = prj.create_sample_id()
        raw_sub_path = Path(sample_id['path'] + '-raw.html')
        prep_sub_path = Path(sample_id['path'] + '-cleaned.txt')
        sub_dir = Path(train_dir, sample_id['dir'])

        # write html file to disc
        full_path = Path(train_dir, raw_sub_path)
        sub_dir.mkdir(exist_ok=True, parents=True)
        try:
            with open(full_path, 'wt') as file:
                file.write(html)
                ok = True
        except BaseException as be:
            print(be)
            ok = False

        # generate preprocessed document and write it to disc
        prepared = html_cleaning.clean_html(html)
        prepared = stops_removal.remove_stop_words(prepared, lang=lang)
        prepared = stemming.stem(prepared, lang=lang)
        full_path = Path(train_dir, prep_sub_path)
        try:
            with open(full_path, 'wt') as file:
                file.write(prepared)
                docs.append(prepared)
        except BaseException as be:
            print(be)
            prep_sub_path = pd.NA  # write NA instead of the sub path

        # add to data collection if writing has succeeded
        if ok:
            dic = {
                'raw file': str(raw_sub_path),
                'prepared file': str(prep_sub_path),
                'origin': 'sample_generator',
                'language': lang,
                'rating': rating,
                'labeled by': 'alg_cat'
            }
            df = pd.DataFrame(dic, index=[sample_id['id']])
            file_data.append(df)
            successes += 1

    print(f'wrote {successes} out of {size} files successfully')

    if len(file_data) < 1:
        return prj

    # concat to single data frame
    file_data = pd.concat(file_data)

    # split to training data and test data
    clean = file_data.dropna()
    train0, test = train_test_split(
        clean.index, test_size=0.2, stratify=clean['rating'])
    train1 = file_data.loc[train0]
    train, val = train_test_split(train1.index, test_size=0.2, stratify=train1['rating'])
    file_data.loc[train, 'usage'] = 'train'
    file_data.loc[test, 'usage'] = 'test'
    file_data.loc[val, 'usage'] = 'validation'

    # determine two vocabularies
    print('number of docs: '+str(len(docs)))
    vocab1 = vocab_extraction.extract_vocab(docs, min_df=3)
    vocab2 = vocab_extraction.extract_vocab(docs, min_df=3, ngram_range=(2, 2))

    # out
    prj.write_training_index(file_data)
    print()
    print(file_data)

    prj.write_vocab(vocab1, 'vocab_monograms')
    print()
    print('monogram vocabulary:')
    print(vocab1)
    prj.write_vocab(vocab2, 'vocab_bigrams')
    print()
    print('bigram vocabulary:')
    print(vocab2)

    return prj
