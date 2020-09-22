import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from collections import Counter

np.random.seed(101)

def load_dataset(path = None):
    if path == None:
        raise ValueError("Path not provided")

    else:
        df = pd.read_csv(path, engine='python')
        df = df.fillna(method = 'ffill')
        group = df.groupby("Sentence #")

        all_sent = []
        all_tags = []

        done = 0

        for _, indices in group.groups.items():
            sentence = df.iloc[indices].Word.values.tolist()
            tags = df.iloc[indices].Tag.values.tolist()
            all_sent.append(sentence)
            all_tags.append(tags)
            
            done += 1
            
            if(done % 500 == 0):
                print(f"Processed {done} sentences", end='\r')
                
        print(f"Total Number of sentences : {done}")

        return all_sent, all_tags

def create_vocabularies(sentences, tags, pad = 0, pad_tag = -1):
    word_counter = Counter()
    tag_counter = Counter()

    for sent in sentences:
        word_counter.update(sent)
        
    for tag in tags:
        tag_counter.update(tag)

    PAD = pad
    UNK = 1
    PAD_TAG = pad_tag

    vocab = {'<unk>' : UNK, '<pad>' : PAD}
    for i, (word, cnt) in enumerate(word_counter.items()):
        vocab[word] = i + 2
        
    tags = {'<pad_tag>' : PAD_TAG}
    for i, (t, c) in enumerate(tag_counter.items()):
        tags[t] = i

    return vocab, tags