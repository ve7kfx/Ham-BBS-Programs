cat news6.py
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import colorama
import textwrap

def fetch_feed(topic):
    """Fetches the news feed based on the user's topic of interest."""
    url = f"https://news.google.com/rss/search?q={topic}"
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
    """Fetches the full content of a news article and its associated image."""
    try:
        response = requests.get(article['link'])
        soup = BeautifulSoup(response.content, 'html.parser')
        article_content = soup.find_all('p')
        text = ' '.join(segment.get_text() for segment in article_content)
        full_article_text = textwrap.fill(text, width=80)

        if 'copyright' in text.lower() or '©' in text:
            return "Sorry, unable to display over ham radio due to copyright concerns."

        # Fetching image URL
        image_tag = soup.find('meta', property='og:image') or soup.find('link', rel='image_src')
        if image_tag and image_tag.get('content'):
            article['media_content'] = image_tag['content']

        return full_article_text
    except Exception as e:
        return "Could not fetch full article content."

def image_to_ascii_art(url):
    """Converts an image URL to ASCII art."""
    ASCII_CHARS = "@%#*+=-:. "
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    image = image.convert('L').resize((80, 30))
    pixels = image.getdata()
    ascii_str = ''
    for pixel in pixels:
        ascii_str += ASCII_CHARS[pixel // 25]
    ascii_str = '\n'.join([ascii_str[i:i+80] for i in range(0, len(ascii_str), 80)])
    return ascii_str

def image_to_ansi_art(url):
    """Converts an image URL to ANSI art."""
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
    """Displays a list of articles for the current page."""
    start = page * per_page
    end = start + per_page
    for i, article in enumerate(articles[start:end]):
        print(f"{i + start + 1}. {article['title']}")

def get_user_topic():
    """Asks the user to input a topic they want to hear news about."""
    topic = input("Enter a topic you want to hear news about: ")
    return topic.strip()

def main():
    """Main function to run the news reader application."""
    colorama.init()

    while True:
        topic = get_user_topic()
        articles = fetch_feed(topic)

        if not articles:
            print("No articles found for this topic.")
            continue

        current_page = 0
        per_page = 5
        total_pages = len(articles) // per_page

        while True:
            display_articles(articles, current_page, per_page)
            print("\nCommands: n (next), p (previous), x (exit), [number] (select article), t (change topic)")
            command = input("Enter command: ")

            if command.lower() == 'x':
                return
            elif command.lower() == 't':
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
