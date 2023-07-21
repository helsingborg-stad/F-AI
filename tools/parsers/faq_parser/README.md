# FAQ parser

Simple Python script for extracting information from an FAQ page in the [Hbg planning permission website](https://helsingborg.se/bo-bygga-och-miljo/bygga-nytt-bygga-om-bygga-till/bygglov-och-anmalan/soka-bygglov-vad-vill-du-gora/) and convert it to a Markdown file. The FAQ information should be contained within HTML divs of a specified class name.

## Requirements
- Python 3.9.6 or higher
- git
- pip

## Usage
1) Download the repository and navigate to the faq_parser folder.

2) Install the requirements `pip3 install -r requirements.txt` and run `python3 faq-scraper.py --help` to print usage.

3) Run command `python3 faq-parser.py --url https://helsingborg.se/bo-bygga-och-miljo/bygga-nytt-bygga-om-bygga-till/bygglov-och-anmalan/soka-bygglov-vad-vill-du-gora/ --class_value sidebar-content-area --output ./output/output.md` to parse and create Markdown output file in folder `./output/output.md`.

There is also a .vscode launcher (.vscode/launch.json) that can be used to running and debugging the script.
The launcher will run the FAQ parser with arguments:
```text
"args": [
                "--url",
                "https://helsingborg.se/bo-bygga-och-miljo/bygga-nytt-bygga-om-bygga-till/bygglov-och-anmalan/soka-bygglov-vad-vill-du-gora/",
                "--class_value",
                "sidebar-content-area",
                "--output",
                "./output/output.md"
            ]
```
