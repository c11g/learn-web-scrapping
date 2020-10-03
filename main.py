from webdev import get_posts
from save import save_to_csv

posts = get_posts()
save_to_csv(posts)