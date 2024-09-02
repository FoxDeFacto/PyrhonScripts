import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from queue import Queue

# Function to fetch and display articles concurrently from Novinky.cz
async def fetch_articles():
    url = "https://www.novinky.cz"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                articles = soup.find_all('h3')  # Find all articles

                categories_of_interest = ["Válka na Ukrajině", "Ekonomika", "Evropa"]

                tasks = [
                    fetch_article_content(session, urljoin(url, link['href']), link.get_text(strip=True), categories_of_interest)
                    for article in articles
                    if (link := article.find('a')) and 'href' in link.attrs and not link['href'].startswith('javascript:')
                ]

                for task in asyncio.as_completed(tasks):
                    article_data = await task
                    if article_data:
                        queue.put(article_data)

    root.after(100, process_queue)

# Function to fetch articles from Pravda.com.ua
async def fetch_articles_pravda():
    url = "https://www.pravda.com.ua"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                articles = soup.find_all('h3')  # Find all article headings

                categories_of_interest = ["війна", "зброя"]

                tasks = [
                    fetch_article_content_pravda(session, urljoin(url, link['href']), link.get_text(strip=True), categories_of_interest)
                    for article in articles
                    if (link := article.find('a')) and 'href' in link.attrs and not link['href'].startswith('javascript:')
                ]

                for task in asyncio.as_completed(tasks):
                    article_data = await task
                    if article_data:
                        queue.put(article_data)

    root.after(100, process_queue)

# Asynchronous function to fetch article content from Novinky.cz with duplicate check
async def fetch_article_content(session, article_url, title, categories_of_interest):
    try:
        async with session.get(article_url) as response:
            if response.status == 200:
                article_soup = BeautifulSoup(await response.text(), 'html.parser')

                breadcrumb_div = article_soup.find('div', class_='g_fC')
                if breadcrumb_div:
                    breadcrumb_spans = breadcrumb_div.find_all('span')
                    categories = [span.get_text(strip=True) for span in breadcrumb_spans[:-1]]
                    filtered_categories = [category for category in categories if category in categories_of_interest or category == "Novinky.cz"]

                    if filtered_categories and any(cat in categories_of_interest for cat in filtered_categories):
                        content_section = article_soup.find('section', class_='j_ir')
                        if content_section:
                            article_text = ""
                            unique_texts = set()
                            for element in content_section.find_all(class_=['e_aY', 'c_aY']):
                                if not element.find_parent(class_=['e_ei', 'e_aW']):
                                    text = element.get_text(strip=True)
                                    if text not in unique_texts:
                                        unique_texts.add(text)
                                        article_text += text + "\n\n"
                            return {
                                "category": "Novinky.cz, " + ", ".join(filtered_categories),
                                "title": title.split('.')[0],
                                "content": article_text.strip()
                            }
    except Exception:
        pass
    return None

# Asynchronous function to fetch article content from Pravda.com.ua with duplicate check
async def fetch_article_content_pravda(session, article_url, title, categories_of_interest):
    try:
        async with session.get(article_url) as response:
            if response.status == 200:
                article_soup = BeautifulSoup(await response.text(), 'html.parser')

                category_div = article_soup.find('div', class_='post_tags')
                if category_div:
                    category_links = category_div.find_all('a')
                    categories = [a.get_text(strip=True) for a in category_links]
                    filtered_categories = [category for category in categories if category in categories_of_interest]

                    if filtered_categories:
                        content_div = article_soup.find('div', class_='post_text')
                        if content_div:
                            article_text = "\n\n".join([p.get_text(strip=True) for p in content_div.find_all('p')])

                            for ul in content_div.find_all('ul'):
                                ul_text = "\n".join([f"- {li.get_text(strip=True)}" for li in ul.find_all('li')])
                                article_text += "\n\n" + ul_text

                            return {
                                "category": "Pravda.com.ua, " + ", ".join(filtered_categories),
                                "title": title,
                                "content": article_text.strip()
                            }
    except Exception:
        pass
    return None

def process_queue():
    while not queue.empty():
        data = queue.get()
        if isinstance(data, dict):
            articles_list.append(data)
            if "Válka na Ukrajině" in data["category"] or "війна" in data["category"]:
                color = "#ff0000"
            elif "Ekonomika" in data["category"]:
                color = "#0000ff"
            elif "Evropa" in data["category"]:
                color = "#008000"
            elif "зброя" in data["category"]:
                color = "#800080"
            else:
                color = "#000000"
            articles_tree.insert("", tk.END, text=data["title"], values=(data["category"],), tags=(color,))

def on_article_select(event):
    selected_item = articles_tree.selection()
    if selected_item:
        index = articles_tree.index(selected_item)
        article = articles_list[index]
        article_details.delete(1.0, tk.END)
        article_details.insert(tk.INSERT, f"[Kategorie]\n", 'category')
        article_details.insert(tk.INSERT, f"{article['category']}\n\n", 'category_content')
        article_details.insert(tk.INSERT, f"[Název]\n", 'title')
        article_details.insert(tk.INSERT, f"{article['title']}\n\n", 'title_content')
        article_details.insert(tk.INSERT, f"[Obsah]\n", 'content')
        article_details.insert(tk.INSERT, f"{article['content']}\n", 'content_content')

# Initialize the main window
root = tk.Tk()
root.title("Zprávy")
root.geometry("900x600")

style = ttk.Style()
style.configure("TFrame", background="#f5f5f5")
style.configure("TLabel", background="#f5f5f5", font=("Segoe UI", 12))
style.configure("Treeview", font=("Segoe UI", 10), background="#f9f9f9", fieldbackground="#f9f9f9", foreground="#000000")
style.configure("Treeview.Heading", font=("Segoe UI", 10, 'bold'), background="#cccccc")

root.columnconfigure(0, weight=1, minsize=150)
root.columnconfigure(1, weight=3)
root.rowconfigure(0, weight=1)

left_frame = ttk.Frame(root, padding="10")
left_frame.grid(row=0, column=0, sticky="ns")

articles_tree = ttk.Treeview(left_frame, columns=("Kategorie",), show="tree headings", height=25)
articles_tree.heading("#0", text="Název", anchor="w")
articles_tree.column("#0", width=150, anchor="w", stretch=True)
articles_tree.heading("Kategorie", text="Kategorie", anchor="w")
articles_tree.column("Kategorie", width=100, anchor="w", stretch=True)
articles_tree.grid(row=0, column=0, sticky="ns")

articles_tree.tag_configure("#ff0000", foreground="#ff0000")
articles_tree.tag_configure("#0000ff", foreground="#0000ff")
articles_tree.tag_configure("#008000", foreground="#008000")
articles_tree.tag_configure("#800080", foreground="#800080")

scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=articles_tree.yview)
articles_tree.config(yscrollcommand=scrollbar.set)
scrollbar.grid(row=0, column=1, sticky="ns")

right_frame = ttk.Frame(root, padding="10")
right_frame.grid(row=0, column=1, sticky="nsew")

article_details = ScrolledText(right_frame, wrap=tk.WORD, font=("Segoe UI", 12), bg="#ffffff", padx=10, pady=10, relief="flat", borderwidth=0)
article_details.grid(row=0, column=0, sticky="nsew")

right_frame.columnconfigure(0, weight=1)
right_frame.rowconfigure(0, weight=1)

article_details.tag_configure('category', font=("Segoe UI", 10, 'bold'), foreground="#ff5722")
article_details.tag_configure('title', font=("Segoe UI", 10, 'bold'), foreground="#2196f3")
article_details.tag_configure('content', font=("Segoe UI", 10, 'bold'), foreground="#673ab7")

article_details.tag_configure('category_content', font=("Segoe UI", 12), foreground="#ff5722")
article_details.tag_configure('title_content', font=("Segoe UI", 12), foreground="#2196f3")
article_details.tag_configure('content_content', font=("Segoe UI", 12), foreground="#333333")

articles_tree.bind('<<TreeviewSelect>>', on_article_select)

articles_list = []
queue = Queue()

async def main():
    await asyncio.gather(fetch_articles(), fetch_articles_pravda())

# Start the main event loop and the async loop
root.after(100, lambda: asyncio.run(main()))
root.mainloop()
