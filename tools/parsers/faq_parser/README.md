# FAQ parser

This repo contains a simple script for parsing and converting [Hbgs planning permission FAQ](https://helsingborg.se/bo-bygga-och-miljo/bygga-nytt-bygga-om-bygga-till/bygglov-och-anmalan/soka-bygglov-vad-vill-du-gora/) to Markdown.

## Prerequisits
- Python 3.6 or higher
- git
- pip

## Example usage
Install the requirements `pip3 install -r requirements.txt` and run `python3 faq-scraper.py --help` to print usage.

Run command `python3 faq-parser.py --url https://helsingborg.se/bo-bygga-och-miljo/bygga-nytt-bygga-om-bygga-till/bygglov-och-anmalan/soka-bygglov-vad-vill-du-gora/ --class_value sidebar-content-area --output ./output/output.md` to parse and create Markdown file in the output folder.

There is also a .vscode launcher (.vscode/launch.json) that can be used to running and debugging the script.
The launcher will run the FAQ parser with arguments:
```json
"args": [
                "--url",
                "https://helsingborg.se/bo-bygga-och-miljo/bygga-nytt-bygga-om-bygga-till/bygglov-och-anmalan/soka-bygglov-vad-vill-du-gora/",
                "--class_value",
                "sidebar-content-area",
                "--output",
                "./output/output.md"
            ],
```
