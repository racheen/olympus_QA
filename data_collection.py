import requests
# import wikipediaapi 
import gutenbergpy.textget
import os
from bs4 import BeautifulSoup

""" 
def fetch_wikipedia_pages(topic_list, save_dir="wikipedia_data"):
    os.makedirs(save_dir, exist_ok=True)
    user_agent = "MyMythologyBot/1.0 (tumu0009@algonquinlive.com)"
    wikipediaapi.set_user_agent(user_agent)  # Set the user agent
    wiki_wiki = wikipediaapi.Wikipedia("en")
    
    for topic in topic_list:
        page = wiki_wiki.page(topic)
        if page.exists():
            with open(os.path.join(save_dir, f"{topic.replace(' ', '_')}.txt"), "w", encoding="utf-8") as f:
                f.write(page.text)
            print(f"Saved Wikipedia page: {topic}")
        else:
            print(f"Page {topic} not found.")
"""
def fetch_gutenberg_text(book_id, save_dir="gutenberg_data"):
    os.makedirs(save_dir, exist_ok=True)
    text = gutenbergpy.textget.get_text_by_id(book_id)
    if text:
        with open(os.path.join(save_dir, f"gutenberg_{book_id}.txt"), "w", encoding="utf-8") as f:
            f.write(text.decode("utf-8"))
        print(f"Saved Gutenberg text: {book_id}")
    else:
        print(f"Gutenberg book {book_id} not found.")

def fetch_theoi_text(url, save_dir="theoi_data"):
    os.makedirs(save_dir, exist_ok=True)
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        text = "\n".join([p.text for p in soup.find_all("p")])
        file_name = os.path.join(save_dir, "theoi_text.txt")
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Saved Theoi data from: {url}")
    else:
        print(f"Failed to fetch Theoi data from: {url}")

if __name__ == "__main__":
    # greek_myth_topics = ["Zeus", "Hera", "Poseidon", "Hades", "Apollo", "Athena", "Aphrodite", "Hermes", "Ares", "Dionysus", "Persephone", "Greek Mythology"]
    # fetch_wikipedia_pages(greek_myth_topics)
    
    gutenberg_books = [14994, 19789]  # Example book IDs: Bulfinch's Mythology, The Library of Apollodorus
    for book_id in gutenberg_books:
        fetch_gutenberg_text(book_id)
    
    theoi_url = "https://www.theoi.com/"  # Example URL
    fetch_theoi_text(theoi_url)
