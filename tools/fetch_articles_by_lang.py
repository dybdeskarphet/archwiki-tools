import requests
import string
import os


def fetch_wiki_source(title):
    url = "https://wiki.archlinux.org/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "revisions",
        "rvprop": "content",
        "rvslots": "*",
    }

    response = requests.get(url, params=params)
    return response.json()


def parse_source(json_response):
    try:
        page = next(iter(json_response["query"]["pages"].values()))
        if "revisions" in page and "slots" in page["revisions"][0]:
            return page["revisions"][0]["slots"]["main"]["*"]
        else:
            return "Page not found or unexpected JSON structure."
    except Exception as e:
        print(f"Error parsing JSON response: {e}")
        return None


def sanitize_title(title):
    turkish_chars = "şğüöçıİ"
    valid_chars = (
        "-_.() "
        + string.ascii_letters
        + string.digits
        + string.whitespace
        + turkish_chars
    )
    filename = "".join(c for c in title if c in valid_chars)
    return filename


def get_directory(title):
    if "(Türkçe)" in title:
        return "tr"
    else:
        return "en"


def save_to_file(content, title):
    dir_name = get_directory(title)

    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    filename = os.path.join(dir_name, sanitize_title(title) + ".wiki")

    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)


def local_content_starts_with_working_on(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()
            return content.startswith("<!-- Working on")
    except FileNotFoundError:
        return False


def main():
    titles = [
        "Installation guide (Türkçe)",
        "Arch compared to other distributions (Türkçe)",
        "Arch Linux (Türkçe)",
        "General recommendations (Türkçe)",
        "Help:Reading (Türkçe)",
        "Nano (Türkçe)",
        "Reflector (Türkçe)",
        "ArchWiki:Translation Team (Türkçe)",
        "USB flash installation medium (Türkçe)",
        "Systemd-timesyncd",
    ]

    for title in titles:
        filename = os.path.join(get_directory(title), sanitize_title(title) + ".wiki")

        if local_content_starts_with_working_on(filename):
            print(f"Skipping update for '{title}' as it's marked as being worked on.")
            continue

        json_response = fetch_wiki_source(title)
        if json_response:
            content = parse_source(json_response)
            if content:
                save_to_file(content, title)
                print(f"Saved {title} to file")
            else:
                print(f"Failed to parse the article source for {title}")
        else:
            print(f"Failed to fetch the article source for {title}")


if __name__ == "__main__":
    main()
