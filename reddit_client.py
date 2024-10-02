import praw
from config import CLIENT_ID, CLIENT_SECRET, USER_AGENT, SUBREDDITS, NUM_POSTS, TIME_FILTER

def get_reddit_instance():
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT
    )
    return reddit

def fetch_top_posts():
    reddit = get_reddit_instance()
    all_posts = []
    for subreddit in SUBREDDITS:
        print(f"Fetching top posts from r/{subreddit}")
        subreddit_instance = reddit.subreddit(subreddit)
        top_posts = subreddit_instance.top(time_filter=TIME_FILTER, limit=NUM_POSTS)
        for post in top_posts:
            post_data = {
                'id': post.id,
                'title': post.title,
                'score': post.score,
                'url': post.url,
                'num_comments': post.num_comments,
                'created_utc': post.created_utc,
                'comments': fetch_comments(post)
            }
            all_posts.append(post_data)
    return all_posts

def fetch_comments(post):
    post.comments.replace_more(limit=0)
    comments = []
    for comment in post.comments.list():
        comments.append({
            'id': comment.id,
            'body': comment.body,
            'score': comment.score,
            'created_utc': comment.created_utc,
            'author': str(comment.author)
        })
    return comments