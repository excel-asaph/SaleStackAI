from bs4 import BeautifulSoup, Tag, NavigableString
from bs4.element import PageElement
import re
import requests
from requests import Response
from requests.exceptions import RequestException, HTTPError
from typing import List, Literal


TAGS: List[str] = ["meta", "style", "script", "link", "head"]
count: int = 0


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-US,en;q=0.9",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
}

with open("sales_page_links.txt", "r", encoding="utf-8") as file:
    for url in file:
        url = url.strip()
        Training_data: str = ""
        try:
            response: Response = requests.get(url, headers=headers)
            response.raise_for_status()
            html_content: bytes = response.content
            soup: BeautifulSoup = BeautifulSoup(html_content, "html.parser")
            current_element: PageElement = soup.html or soup.body or soup.contents[0]
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            continue
        except RequestException as e:
            print(f"Request error occurred: {e}")
            continue
        
        while current_element is not None:
            if isinstance(current_element, NavigableString):
                parent_element: PageElement = current_element.parent
                if isinstance(parent_element, Tag) and str(parent_element.name) not in TAGS:
                    tag_before_text: str = f"[{str(parent_element.name)}]"
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
        with open(file_name, "w", encoding="utf-8") as fp:
            fp.write(Training_data)
        count += 1
