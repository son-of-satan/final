#!/usr/bin/env python3

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import pandas as pd
from pandarallel import pandarallel
from ast import literal_eval

pandarallel.initialize(progress_bar=True)

import nltk

nltk.download("punkt")


def get_data(filepath):
    df = pd.read_csv(filepath)
    df = df[df["Text"].notna() & df["Genres"].notna()]
    df["Genres"] = df["Genres"].apply(lambda x: literal_eval(x))
    df = df[df["Genres"].astype(bool)]
    return df


df = get_data("~/Downloads/dataset-preprocessed.csv")
df = df[df["Chunk Word Count"] < 16000]

tokenizer = Tokenizer("english")
stemmer = Stemmer("english")
summarizer = TextRankSummarizer(stemmer)
summarizer.stop_words = get_stop_words("english")


def summarize_text(text, target_len):
    if len(text.split()) < 4000:
        return text

    parser = PlaintextParser.from_string(text, tokenizer)
    return "".join(
        [str(sentence) for sentence in summarizer(parser.document, target_len)]
    )


df["Summary"] = df["Text"][:].parallel_apply(lambda x: summarize_text(x, 75))
df["Summary Word Count"] = df["Summary"].parallel_apply(lambda x: len(x.split()))

df.to_csv("./data/summarized.csv")
