#!/usr/bin/env python3

import argparse
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import urllib.parse
import json
import gutenbergpy.textget


parser = argparse.ArgumentParser(
    description="Gather data from Project Gutenberg and Goodreads"
)

parser.add_argument(
    "-C",
    "--catalog",
    default="/media/son-of-satan/hoard/gutenberg/pg_catalog.csv",
)

parser.add_argument("-s", "--source")
parser.add_argument("-t", "--target", required=True)
parser.add_argument("-c", "--count", type=int, default=10)

args = parser.parse_args()


def get_book_url(title, authors):
    search_params = urllib.parse.urlencode({"q": title, "search_type": "books"})
    search_url = f"https://www.goodreads.com/search?{search_params}"

    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, features="lxml")

    return soup.find(class_="bookTitle")["href"]


def get_book_genres(title, authors):
    book_url = f"https://www.goodreads.com/{get_book_url(title, authors)}"
    response = requests.get(book_url)
    soup = BeautifulSoup(response.text, features="lxml")

    data = soup.find(id="__NEXT_DATA__")
    apolloState = json.loads(data.contents[0])["props"]["pageProps"]["apolloState"]

    genres = []
    for key in apolloState:
        if key.startswith("Book"):
            for bookGenre in apolloState[key]["bookGenres"]:
                genres.append(bookGenre["genre"]["name"])

    return genres


def get_book_text(text_id):
    raw = gutenbergpy.textget.get_text_by_id(text_id)
    clean = gutenbergpy.textget.strip_headers(raw).decode("utf-8")

    return clean


catalog_df = pd.read_csv(args.catalog, low_memory=False, index_col="Text#")

# filter English fiction
catalog_df = catalog_df[catalog_df["Language"].str.contains("en")]
catalog_df = catalog_df[
    catalog_df["Subjects"].str.contains("fiction", case=False, na=False)
]

source_df = (
    pd.read_csv(args.source, index_col="Text#")[["Text", "Genres"]]
    if args.source
    else pd.DataFrame(columns=["Text#", "Text", "Genres"]).set_index("Text#")
)

target_df = catalog_df.join(source_df)
null_df = target_df[target_df["Text"].isnull() | target_df["Genres"].isnull()]
null_df = null_df[: args.count]
notnull_df = target_df[target_df["Text"].notnull() & target_df["Genres"].notnull()]

genres = []
text = []

for index, row in null_df.iterrows():
    text_id = index
    title = row["Title"]
    authors = row["Authors"]
    book_genres = row["Genres"]
    book_text = row["Text"]

    print(f"Retrieving genres/text for {text_id}, {title}")

    try:
        if pd.isna(book_genres):
            book_genres = get_book_genres(title, authors)

        if pd.isna(book_text):
            book_text = get_book_text(text_id)
    except Exception as e:
        print(f"Couldn't retrieve genres/text for {title}: {e}")

    genres.append(book_genres)
    text.append(book_text)


null_df["Text"] = text
null_df["Genres"] = genres

target_df = pd.concat([notnull_df, null_df])

target_df.to_csv(args.target)
