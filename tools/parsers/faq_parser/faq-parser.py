import requests
from bs4 import BeautifulSoup
import html2text
import argparse
import time

# setup command line arguments
parser = argparse.ArgumentParser(description='Convert Hbg planning permission FAQ to Markdown')
parser.add_argument('--url', type=str, help='The URL to parse')
parser.add_argument('--class_value', type=str, help='The HTML class containing the FAQ')
parser.add_argument('--output_file', type=str, default='output.md', help='The output Markdown file name')

args = parser.parse_args()

url = args.url
class_value = args.class_value
output_file = args.output_file

# parse the HTML
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# we only want the accordions containing the FAQ
element = soup.find('div', {'class': class_value})

# convert the HTML to Markdown
h = html2text.HTML2Text()
h.ignore_links = True       # remove all hyperlinks from text

markdown = h.handle(element.prettify())

# post-process the markdown and convert accordions to h1 headers
# the accordions are converted from HTML to text '<some title>  keyboard_arrow_down'
# we want to post-process '<some title>  keyboard_arrow_down' to '# <some title>'
lines = markdown.split('\n')
processed_lines = []

for line in lines:
    if line.endswith('keyboard_arrow_down'):
        processed_lines.append('# ' + line.replace('keyboard_arrow_down', ''))
    else:
        processed_lines.append(line)

processed_markdown = '\n'.join(processed_lines)

# save the markdown to a file
# filename can be set by the user, default is output.md
with open(output_file, 'w') as f:
    f.write(processed_markdown)

print(f"Markdown file saved as {output_file}")