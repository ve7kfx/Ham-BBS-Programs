import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import colorama
import textwrap

CATEGORIES = ['Technology', 'Sports', 'World', 'Business', 'Entertainment', 'Science']

def fetch_feed(category):
    url = f"https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en&topic={category[0].lower()}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'xml')
    articles = []
    for item in soup.find_all('item'):
        article = {
            'title': item.title.get_text(),
            'summary': item.description.get_text(),
            'link': item.link.get_text(),
            'media_content': None
        }
        articles.append(article)
    return articles

def fetch_full_article_and_image(article):
    try:
        response = requests.get(article['link'])
        soup = BeautifulSoup(response.content, 'html.parser')
        article_content = soup.find_all('p')
        text = ' '.join(segment.get_text() for segment in article_content)
        full_article_text = textwrap.fill(text, width=80)

        if 'copyright' in text.lower() or '©' in text:
            return "Sorry, unable to display over ham radio due to copyright concerns."

        image_tag = soup.find('meta', property='og:image') or soup.find('link', rel='image_src')
        if image_tag and image_tag.get('content'):
            article['media_content'] = image_tag['content']

        return full_article_text
    except Exception as e:
        return "Could not fetch full article content."

def image_to_ascii_art(url):
    ASCII_CHARS = "@%#*+=-:. "
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    image = image.convert('L').resize((80, 30))
    pixels = image.getdata()
    ascii_str = ''
    for pixel in pixels:
        index = pixel * len(ASCII_CHARS) // 256  # Corrected indexing formula
        ascii_str += ASCII_CHARS[index]
    ascii_str = '\n'.join([ascii_str[i:i+80] for i in range(0, len(ascii_str), 80)])
    return ascii_str

def image_to_ansi_art(url):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    image = image.resize((80, 30))
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

def main_menu():
    print("Select a news category:")
    for i, category in enumerate(CATEGORIES):
        print(f"{i + 1}. {category}")

    category_choice = input("Enter your choice (number): ")
    try:
        selected_category = CATEGORIES[int(category_choice) - 1]
    except (IndexError, ValueError):
        print("Invalid choice. Defaulting to World news.")
        selected_category = "World"

    return fetch_feed(selected_category)

def main():
    colorama.init()

    while True:
        articles = main_menu()

        if not articles:
            print("No articles found.")
            return

        current_page = 0
        per_page = 5
        total_pages = len(articles) // per_page

        while True:
            display_articles(articles, current_page, per_page)
            print("\nCommands: n (next), p (previous), x (exit), [number] (select article), m (main menu)")
            command = input("Enter command: ")

            if command.lower() == 'x':
                return
            elif command.lower() == 'm':
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
                    full_content = fetch_full_article_and_image(article)
                    print(full_content)

                    if article['media_content']:
                        print("\nImage display options:\n1. ANSI\n2. ASCII\n3. None")
                        image_choice = input("Choose an option (1/2/3): ")
                        if image_choice == '1':
                            print(image_to_ansi_art(article['media_content']))
                        elif image_choice == '2':
                            print(image_to_ascii_art(article['media_content']))

                    input("Press Enter to continue...")

if __name__ == "__main__":
    main()
