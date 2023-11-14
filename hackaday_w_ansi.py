import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import colorama
import textwrap

def fetch_feed(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'xml')
    articles = []
    for item in soup.find_all('item'):
        article = {
            'title': item.title.get_text(),
            'summary': item.description.get_text(),
            'link': item.link.get_text(),
            'media_content': item.find('media:content')['url'] if item.find('media:content') else None
        }
        articles.append(article)
    return articles

def fetch_full_article(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    article_content = soup.find('article')
    if article_content:
        text = ' '.join(article_content.get_text().split())
        # Wrap text to 80 characters per line
        return textwrap.fill(text, width=80)
    else:
        return "Article content not found."

def image_to_ansi_art(url):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    image = image.resize((80, 30))  # Resize for reasonable ANSI art size
    art = ''
    for y in range(image.height):
        for x in range(image.width):
            pixel = image.getpixel((x, y))
            art += '\x1b[48;2;{};{};{}m \x1b[0m'.format(*pixel)
        art += '\n'
    return art

def display_articles(articles, page, per_page):
    start = page * per_page
    end = start + per_page
    for i, article in enumerate(articles[start:end]):
        print(f"{i + start + 1}. {article['title']}")

def main():
    colorama.init()  # Initialize colorama
    feed_url = "https://hackaday.com/blog/feed/"
    articles = fetch_feed(feed_url)

    current_page = 0
    per_page = 5
    total_pages = len(articles) // per_page

    while True:
        display_articles(articles, current_page, per_page)
        print("\nCommands: n (next), p (previous), q (quit), [number] (select article)")
        command = input("Enter command: ")

        if command == 'q':
            break
        elif command == 'n':
            if current_page < total_pages:
                current_page += 1
        elif command == 'p':
            if current_page > 0:
                current_page -= 1
        elif command.isdigit():
            article_index = int(command) - 1
            if 0 <= article_index < len(articles):
                article = articles[article_index]
                print("\n" + article['title'] + "\n")
                full_content = fetch_full_article(article['link'])
                print(full_content)
                show_image = input("Show image? (y/n): ").lower() == 'y'
                if show_image and article['media_content']:
                    print(image_to_ansi_art(article['media_content']))
                input("Press Enter to continue...")

main()
