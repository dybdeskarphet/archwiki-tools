# ArchWiki Tools 🛠

This repository contains a collection of tools designed to enhance the experience of using and contributing to the Arch Linux Wiki (ArchWiki). These tools are developed to assist in tasks such as copying revision numbers, fetching and saving wiki content, and tracking changes in Turkish articles.

## Tools Included

### 1. ArchWiki Copy Revision Number UserScript 📋

A userscript that adds a Floating Action Button (FAB) to ArchWiki pages, allowing users to easily copy the revision number of the current page to the clipboard. This is particularly useful for editors and contributors who need to reference specific revisions.

#### Features:

- Easy extraction and copying of the revision number.
- Visual feedback with a toast message upon successful copy or failure.
- Seamless integration into the ArchWiki interface.

#### Usage:

Install this script as a browser userscript to activate the copy button on ArchWiki pages.

### 2. ArchWiki Article Fetcher and Saver 📥

A Python script that automates the process of fetching and saving the source of ArchWiki articles. It's particularly useful for offline reading or backup purposes.

#### Features:

- Fetches the latest content of specified ArchWiki articles.
- Saves articles in a structured directory format.
- Handles both English and Turkish articles.
- Avoids overwriting articles marked as being worked on.

#### Usage:

Run the script with a list of desired article titles. The script fetches and saves the articles in the appropriate language directory.

### 3. ArchWiki Turkish Articles Tracker 🔎

A Python script to track the latest changes in Turkish articles on ArchWiki. It fetches a list of all Turkish articles, retrieves the last non-bot revision for each, and exports the data to a CSV file.

#### Features:

- Fetches a comprehensive list of Turkish articles from ArchWiki.
- Identifies the latest human-made revision for each article.
- Exports the data to a CSV file for easy tracking and analysis.

#### Usage:

Execute the script to generate a CSV file containing the latest revision information for all Turkish articles on ArchWiki.

## Installation and Dependencies 💻

- The userscript can be installed on any modern browser that supports userscripts (e.g., via Tampermonkey or Greasemonkey).
- Python scripts require Python 3 and the `requests` library.

## Contributing 🤝

Contributions to this project are welcome. Please feel free to fork the repository, make your changes, and submit a pull request.

## License 📄

This project is released under the [GNU GPLv3](LICENSE).
