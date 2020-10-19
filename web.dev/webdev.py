import requests
from bs4 import BeautifulSoup

DOMAIN = "https://web.dev"
BLOG_URL = "https://web.dev/blog/"

def get_soup(url):
  res = requests.get(url)
  return BeautifulSoup(res.text, 'html.parser')

def get_post(soup):
  title = soup.find("h2").text.strip()
  date = soup.find("time").text.strip()
  path = soup.find("a")["href"]
  return {
    "title": title,
    "date": date,
    "link": DOMAIN+path
  }

def get_posts_in_page(page_url):
  posts = []
  soup = get_soup(page_url)
  print(f"Scrapping {page_url}")
  for post_soup in soup.find_all("div", {"class": "w-card"}):
    post = get_post(post_soup)
    posts.append(post)
  return posts

def get_last_page():
  soup = get_soup(BLOG_URL)
  pages = soup.find("nav", {"class": "w-pagination"}).find_all("a")
  page_list = []
  for page in pages:
    page = page.text.strip()
    if(page == ''):
      break
    page_list.append(page)
  return int(max(page_list))

def get_posts():
  posts = []
  total_page = get_last_page()
  
  for page in range(1, total_page+1):
    if(page == 1):
      url = BLOG_URL
    else:
      url = f"https://web.dev/blog/{page}"
    
    list_in_page = get_posts_in_page(url)
    posts = posts + list_in_page

  return posts