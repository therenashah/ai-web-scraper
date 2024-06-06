import asyncio
import pprint
from typing import List
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright


def remove_unwanted_tags(html_content, unwanted_tags=["script", "style"]):

    soup = BeautifulSoup(html_content, 'html.parser')

    for tag in unwanted_tags:
        for element in soup.find_all(tag):
            element.decompose()

    return str(soup)


def extract_tags(html_content, tags: List[str]):
    """
    This takes in HTML content and a list of tags, and returns a string
    containing the text content of all elements with those tags, along with their href attribute if the
    tag is an "a" tag.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    text_parts = []

    for tag in tags:
        elements = soup.find_all(tag)
        for element in elements:
            # If the tag is a link (a tag), append its href as well
            if tag == "a":
                href = element.get('href')
                if href:
                    text_parts.append(f"{element.get_text()} ({href})")
                else:
                    text_parts.append(element.get_text())
            else:
                text_parts.append(element.get_text())

    return ' '.join(text_parts)

def extract_images(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    img_links = []
    elements = soup.find_all('img')
    for element in elements:
        src = element.get('src')
        if src: img_links.append(f"{element.get_text()} ({src})")
    return ''.join(img_links)




def remove_unessesary_lines(content):
    # Split content into lines
    lines = content.split("\n")

    # Strip whitespace for each line
    stripped_lines = [line.strip() for line in lines]

    # Filter out empty lines
    non_empty_lines = [line for line in stripped_lines if line]

    # Remove duplicated lines (while preserving order)
    seen = set()
    deduped_lines = [line for line in non_empty_lines if not (
        line in seen or seen.add(line))]

    # Join the cleaned lines without any separators (remove newlines)
    cleaned_content = "".join(deduped_lines)

    return cleaned_content


async def ascrape_playwright(url, tags: List[str] = ["h1", "h2", "h3", "span", "img", "body"]) -> str:
    """
    An asynchronous Python function that uses Playwright to scrape
    content from a given URL, extracting specified HTML tags and removing unwanted tags and unnecessary
    lines.
    """
    print("Started scraping...")
    results = ""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        try:
            page = await browser.new_page()
            await page.goto(url)

            page_source = await page.content()
            print("extracting images...")
            images = extract_images(page_source)
            print("extracted images...")
            print("scrapping content...")
            results = remove_unessesary_lines(extract_tags(remove_unwanted_tags(page_source), tags))
            results = images+results
            print("Content scraped")
        except Exception as e:
            results = f"Error: {e}"
        await browser.close()
    return results


# TESTING
if __name__ == "__main__":
    url = "https://www.mansworldindia.com/covers/drill-thrills-with-parmish-verma"

    async def scrape_playwright():
        results = await ascrape_playwright(url)
        print(results)

    pprint.pprint(asyncio.run(scrape_playwright()))
