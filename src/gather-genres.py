import pandas as pd

df = pd.read_csv("/media/son-of-satan/hoard/gutenberg/pg_catalog.csv", low_memory=False)

en_df = df[df["Language"].str.contains("en")]
en_fiction_df = en_df[en_df["Subjects"].str.contains("fiction", case=False, na=False)]

print(en_fiction_df.info())

from bs4 import BeautifulSoup
import requests
import json

root_url = "https://www.goodreads.com"

def get_book_url(title, authors):
    search_url = f"{root_url}/search?q={title}&search_type=books"

    response = requests.get(search_url)
    soup = BeautifulSoup(response.text)

    return soup.find(class_="bookTitle")["href"]

def get_book_genres(title, authors):
    book_url = f"{root_url}/{get_book_url(title, authors)}"
    response = requests.get(book_url)
    soup = BeautifulSoup(response.text)

    data = soup.find(id="__NEXT_DATA__")
    apolloState = json.loads(data.contents[0])["props"]["pageProps"]["apolloState"]

    genres = []
    for key in apolloState:
        if key.startswith("Book"):
            for bookGenre in apolloState[key]["bookGenres"]:
                genres.append(bookGenre["genre"]["name"])

    return genres

genres_list = []

for index, row in en_fiction_df[110:300].iterrows():
    text_id, title, authors = row["Text#"], row["Title"], row["Authors"]

    genres = None
    try:
        genres = get_book_genres(title, authors)
    except:
        pass

    genres_list.append({"Text#": text_id, "Title": title, "Genres": genres})

genres_df = pd.DataFrame(genres_list)
genres_df = genres_df.set_index("Text#")
genres_df.to_csv("data/genres-110:300.csv")
