from datetime import datetime
from numpy import genfromtxt
import csv
import os
import pandas as pd
import dataframe_image as dfi
import requests
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.table import Table
from IPython.display import display, HTML


def get_turkish_articles():
    print("Fetching Turkish articles...")
    S = requests.Session()
    URL = "https://wiki.archlinux.org/api.php"

    """ All namespaces available from ArchWiki
    Namespace ID: -2, Name: Media
    Namespace ID: -1, Name: Special
    Namespace ID: 0, Name:
    Namespace ID: 1, Name: Talk
    Namespace ID: 2, Name: User
    Namespace ID: 3, Name: User talk
    Namespace ID: 4, Name: ArchWiki
    Namespace ID: 5, Name: ArchWiki talk
    Namespace ID: 6, Name: File
    Namespace ID: 7, Name: File talk
    Namespace ID: 8, Name: MediaWiki
    Namespace ID: 9, Name: MediaWiki talk
    Namespace ID: 10, Name: Template
    Namespace ID: 11, Name: Template talk
    Namespace ID: 12, Name: Help
    Namespace ID: 13, Name: Help talk
    Namespace ID: 14, Name: Category
    Namespace ID: 15, Name: Category talk
    Namespace ID: 3000, Name: DeveloperWiki
    Namespace ID: 3001, Name: DeveloperWiki talk
    """
    namespaces = [0, 12, 4]
    turkish_articles = []

    try:
        for ns in namespaces:
            PARAMS = {
                "action": "query",
                "format": "json",
                "list": "allpages",
                "apnamespace": ns,
                "aplimit": "max",
            }

            while True:
                response = S.get(url=URL, params=PARAMS)
                response.raise_for_status()
                data = response.json()

                pages = data["query"]["allpages"]
                for page in pages:
                    if page["title"].endswith("(Türkçe)"):
                        turkish_articles.append(
                            {"title": page["title"], "pageid": page["pageid"]}
                        )

                if "continue" not in data:
                    break

                PARAMS["apcontinue"] = data["continue"]["apcontinue"]

        print(f"Found {len(turkish_articles)} Turkish articles.")
        return turkish_articles
    except Exception as e:
        print(f"Error fetching Turkish articles: {e}")
        return []


known_bots = ["Lahwaacz.bot", "Kynikos.bot"]


def get_last_revision_info(pageid):
    S = requests.Session()
    URL = "https://wiki.archlinux.org/api.php"

    PARAMS = {
        "action": "query",
        "format": "json",
        "prop": "revisions",
        "pageids": pageid,
        "rvlimit": 10,  # This option limits the revisions to check, increase it if necessary
        "rvprop": "timestamp|user|comment",
        "rvdir": "older",
    }

    try:
        response = S.get(url=URL, params=PARAMS)
        response.raise_for_status()
        data = response.json()

        revisions = data["query"]["pages"][str(pageid)]["revisions"]
        for revision in revisions:
            if revision["user"] not in known_bots:
                return {
                    "timestamp": revision["timestamp"],
                    "user": revision["user"],
                    "comment": revision.get("comment", "No comment"),
                }
        return None
    except Exception as e:
        print(f"Error fetching revision info for page {pageid}: {e}")
        return None


def write_to_csv(articles, filename="turkish_articles.csv"):
    with open(filename, "r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        data = list(reader)

    wiki_filename = filename.replace(".csv", ".wiki")
    with open(wiki_filename, "w", encoding="utf-8") as wiki_file:
        wiki_file.write(
            '{| class="wikitable"\n! Title !! Timestamp !! User !! Comment\n'
        )
        for row in data:
            wiki_row = "|-\n| " + " || ".join(row.values()) + "\n"
            wiki_file.write(wiki_row)
        wiki_file.write("|}\n")

    md_filename = filename.replace(".csv", ".md")
    with open(md_filename, "w", encoding="utf-8") as md_file:
        md_file.write("| Title | Timestamp | User | Comment |\n")
        md_file.write("|---|---|---|---|\n")
        for row in data:
            md_row = "| " + " | ".join(row.values()) + " |\n"
            md_file.write(md_row)

    print(f"Data written to {filename}, {wiki_filename}, and {md_filename}")


def main():
    turkish_articles = get_turkish_articles()

    if not turkish_articles:
        print("No Turkish articles found or an error occurred.")
        return

    print("Fetching revision info for each article...")
    articles_with_revision = []
    for index, article in enumerate(turkish_articles, start=1):
        print(f"Processing {index}/{len(turkish_articles)}: {article['title']}")
        revision_info = get_last_revision_info(article["pageid"])
        if revision_info:
            articles_with_revision.append({"title": article["title"], **revision_info})

    if articles_with_revision:
        sorted_articles = sorted(
            articles_with_revision,
            key=lambda k: datetime.strptime(k["timestamp"], "%Y-%m-%dT%H:%M:%SZ"),
            reverse=True,
        )
        write_to_csv(sorted_articles)
    else:
        print("No revision data found for the articles.")


if __name__ == "__main__":
    main()
