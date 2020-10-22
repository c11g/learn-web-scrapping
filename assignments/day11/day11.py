import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

"""
When you try to scrape reddit make sure to send the 'headers' on your request.
Reddit blocks scrappers so we have to include these headers to make reddit think
that we are a normal computer and not a python script.
How to use: requests.get(url, headers=headers)
"""

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}


"""
All subreddits have the same url:
i.e : https://reddit.com/r/javascript
You can add more subreddits to the list, just make sure they exist.
To make a request, use this url:
https://www.reddit.com/r/{subreddit}/top/?t=month
This will give you the top posts in per month.
"""

subreddits = [
  "javascript",
  "reactjs",
  "reactnative",
  "programming",
  "css",
  "golang",
  "flutter",
  "rust",
  "django"
]

def make_url(subreddit):
  return f"https://www.reddit.com/r/{subreddit}/top/?t=month"

def get_post(subreddit):
  url = make_url(subreddit)
  raw_html = requests.get(url, headers=headers).text
  soup = BeautifulSoup(raw_html, "html.parser")
  posts = soup.select(".Post")
  
  result = []
  for post in posts:
    try:
      vote = int(post.select_one("._1rZYMD_4xY3gRcSS3p8ODO").string)
      title = post.select_one("h3._eYtD2XCVieq6emjKBH3m").string
      url = post.select_one("a.SQnoC3ObvgnGjWt90zD9Z._2INHSNB8V5eaWp4P0rY_mE").get("href")
    except: continue
    result.append((subreddit, vote, title, url))

  return result
    
app = Flask("DayEleven")

@app.route("/")
def home():
  return render_template(
    "home.html",
    subreddits=subreddits
  )

@app.route("/read")
def read():
  subreddits = list(request.args)

  result = []
  for subreddit in subreddits:
    posts = get_post(subreddit)
    result += posts

  result.sort(key=lambda item: item[1], reverse=True)

  return render_template(
    "read.html",
    args = subreddits,
    result=result
  )

app.run(host="0.0.0.0")