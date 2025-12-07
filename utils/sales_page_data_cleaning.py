from bs4 import BeautifulSoup, Tag, NavigableString
from bs4.element import PageElement
import re
import requests
from requests import Response
from requests.exceptions import RequestException, HTTPError
from typing import List, Literal

URLS: List[str] = ["https://danlokshop.com/collections/coaching-certification-program/products/high-income-copywriter/"]
Training_data: str = ""
TAGS: List[str] = ["meta", "style", "script", "link", "head"]
count: int = 0

for url in URLS:
    try:
        response: Response = requests.get(url)
        response.raise_for_status()
        html_content: bytes = response.content
        soup: BeautifulSoup = BeautifulSoup(html_content, "html.parser")
        current_element: PageElement = soup.html or soup.body or soup.contents[0]
    except HTTPError as http_err:
        continue
    except RequestException as e:
        continue
    
    while current_element is not None:
        if isinstance(current_element, NavigableString):
            previous_element: BeautifulSoup = current_element.previous_element
            if isinstance(previous_element, Tag) and str(previous_element.name) not in TAGS:
                tag_before_text: str = f"[{str(previous_element.name)}]"
                text_after_tag: str = str(current_element.strip())
                if text_after_tag:
                    Training_data += tag_before_text + text_after_tag
            if current_element.next_element is not None:
                Training_data += "\n"
        current_element: BeautifulSoup = current_element.next_element

    Training_data: str = Training_data.replace("\n", "")
    pattern: Literal['(.*?)(?=\[+?[A-Za-z0-9]+\]+?)'] = r'(.*?)(?=\[+?[A-Za-z0-9]+\]+?)'
    replacement: Literal['\g<1>\n'] = r'\g<1>\n'
    Training_data: str = re.sub(pattern, replacement, Training_data)
    Training_data: str = Training_data.replace("\n\n", "\n")
    Training_data: str = re.sub(r'^\n', r'', Training_data)
    file_name: str = f"train_{count}.txt"
    with open(file_name, "+w", encoding="utf-8") as fp:
        fp.write(Training_data)
    count += 1
